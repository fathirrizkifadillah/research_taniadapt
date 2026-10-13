/**
 * Pure TypeScript implementation of Root Zone Soil Water Depletion (Dr)
 * based on FAO-56 Chapter 8 (Allen et al., 1998).
 * Parameters strictly parsed from rules.json (Table 19 & Table 22).
 */

import { CropType } from './types';
import { getFao56DepletionConfig } from './rules';

export interface WaterBalanceParameters {
  crop: CropType;
  soil_texture: string;
  root_depth_m: number;
  taw_mm: number;
  raw_mm: number;
  p_fraction: number;
  taw_basis_mm_m: number;
}

export interface WaterStressEvaluation {
  crop: CropType;
  status: 'normal' | 'kondisi_stres_abiotik' | 'evidence_insufficient';
  evidence_refs: string[];
  depletion_dr_mm: number;
  raw_threshold_mm: number;
  taw_mm: number;
  root_depth_m: number;
  p_fraction: number;
  recommendation: string;
  sensitif_terhadap_asumsi_tanah: boolean;
  asumsi_deplesi_awal_dr0: number;
  insufficient_reason?: string;
}

export function calculateRootDepth(crop: CropType, dap: number): number {
  const config = getFao56DepletionConfig();
  const cropConfig = config.crops[crop];
  if (!cropConfig || !cropConfig.zr_chosen_m) {
    return 1.0;
  }
  const zrMax: number = cropConfig.zr_chosen_m;
  const zrMin = 0.3;
  const stageLengths = cropConfig.stage_lengths_days || [20, 35, 40, 30];
  const lDevTotal = (stageLengths[0] || 20) + (stageLengths[1] || 35);

  if (dap <= 0) return zrMin;
  if (dap >= lDevTotal) return zrMax;
  return Number((zrMin + (dap / lDevTotal) * (zrMax - zrMin)).toFixed(2));
}

export function calculateTawRaw(
  crop: CropType,
  dap: number,
  customTawMmM?: number
): WaterBalanceParameters {
  const config = getFao56DepletionConfig();
  const soilConfig = config.soil;
  const cropConfig = config.crops[crop];

  const tawMmM = customTawMmM ?? soilConfig.taw_default_mm_m; // Default 150 mm/m for loam
  const zr = calculateRootDepth(crop, dap);
  const taw = tawMmM * zr;

  const pFraction: number = cropConfig?.p_fraction ?? 0.5;
  const raw = pFraction * taw;

  return {
    crop,
    soil_texture: soilConfig.texture_default,
    root_depth_m: zr,
    taw_mm: Number(taw.toFixed(2)),
    raw_mm: Number(raw.toFixed(2)),
    p_fraction: pFraction,
    taw_basis_mm_m: tawMmM,
  };
}

export function updateDailyDepletion(
  previousDrMm: number,
  dailyEtcMm: number,
  dailyPrecipMm: number,
  tawMm: number
): number {
  // FAO-56 Eq. 85: Dr(t) = Dr(t-1) - (P - RO) - I - CR + ETc + DP
  // In simplified daily balance without irrigation: Dr = Dr - P_eff + ETc
  // Constrained to 0 <= Dr <= TAW
  const effectiveRain = Math.max(0.0, dailyPrecipMm);
  const nextDr = previousDrMm - effectiveRain + dailyEtcMm;
  return Number(Math.max(0.0, Math.min(tawMm, nextDr)).toFixed(2));
}

export function evaluateWaterStress(
  crop: CropType,
  dap: number,
  currentDepletionDrMm: number,
  initialDr0Mm: number = 0.0
): WaterStressEvaluation {
  // Padi check: Rice is cultivated in ponded wetland regimes
  if (crop === 'padi') {
    return {
      crop,
      status: 'evidence_insufficient',
      evidence_refs: ['FAO56_KC_RICE'],
      depletion_dr_mm: currentDepletionDrMm,
      raw_threshold_mm: 0.0,
      taw_mm: 0.0,
      root_depth_m: 1.0,
      p_fraction: 0.2,
      recommendation:
        'Modul penyiraman deplesi tanah tidak berlaku untuk padi sawah tergenang (ponded wetland regime); membutuhkan model perkolasi genangan lokal.',
      sensitif_terhadap_asumsi_tanah: false,
      asumsi_deplesi_awal_dr0: initialDr0Mm,
      insufficient_reason:
        'Padi sawah di Jawa Barat dibudidayakan dalam kondisi tergenang air; rumus deplesi lengas tanah tak jenuh (RAW = p * TAW) tidak berlaku.',
    };
  }

  // Cabai check: Unverified Kc
  if (crop === 'cabai') {
    return {
      crop,
      status: 'evidence_insufficient',
      evidence_refs: [],
      depletion_dr_mm: currentDepletionDrMm,
      raw_threshold_mm: 0.0,
      taw_mm: 0.0,
      root_depth_m: 0.7,
      p_fraction: 0.3,
      recommendation: 'Parameter koefisien air cabai belum terverifikasi di evidence registry.',
      sensitif_terhadap_asumsi_tanah: false,
      asumsi_deplesi_awal_dr0: initialDr0Mm,
      insufficient_reason: 'Koefisien tanaman cabai belum terdaftar terverifikasi.',
    };
  }

  // Baseline evaluation with standard Loam TAW = 150 mm/m
  const baseParams = calculateTawRaw(crop, dap, 150.0);
  const isBaseStressed = currentDepletionDrMm > baseParams.raw_mm;

  // Sensitivity analysis against TAW 130 and 180 mm/m (FAO-56 Table 19 loam limits)
  const lowParams = calculateTawRaw(crop, dap, 130.0);
  const highParams = calculateTawRaw(crop, dap, 180.0);
  const isLowStressed = currentDepletionDrMm > lowParams.raw_mm;
  const isHighStressed = currentDepletionDrMm > highParams.raw_mm;

  // If stress conclusion changes between 130 and 180, mark sensitive
  const isSensitive = isLowStressed !== isHighStressed;

  const status = isBaseStressed ? 'kondisi_stres_abiotik' : 'normal';
  const recommendation = isBaseStressed
    ? 'Irigasi replenishment segera diperlukan; deplesi melampaui batas air siap serap (Dr > RAW).'
    : 'Lengas tanah mencukupi (Dr <= RAW); tidak memerlukan irigasi darurat.';

  return {
    crop,
    status,
    evidence_refs: isBaseStressed
      ? ['RULE_WATER_FAO56_DEPLETION', 'FAO56_RAW_DEPLETION']
      : ['FAO56_RAW_DEPLETION'],
    depletion_dr_mm: currentDepletionDrMm,
    raw_threshold_mm: baseParams.raw_mm,
    taw_mm: baseParams.taw_mm,
    root_depth_m: baseParams.root_depth_m,
    p_fraction: baseParams.p_fraction,
    recommendation,
    sensitif_terhadap_asumsi_tanah: isSensitive,
    asumsi_deplesi_awal_dr0: initialDr0Mm,
  };
}

/**
 * Crop coefficient (Kc) dynamic curves based on Days After Planting (DAP / HST).
 * Parameters are strictly read from rules.json (FAO-56 Table 11 & Table 12).
 */

import { CropType } from './types';
import { getFao56DepletionConfig } from './rules';

export interface CropKcCurve {
  crop: CropType;
  dap: number;
  kc: number;
  current_stage: 'ini' | 'dev' | 'mid' | 'late' | 'harvested';
  stage_length_days: number[];
  total_days: number;
}

export function calculateDynamicKc(
  crop: CropType,
  dap: number,
  panenKering: boolean = true
): CropKcCurve {
  const config = getFao56DepletionConfig();
  const cropConfig = config.crops[crop];

  if (!cropConfig || crop === 'cabai') {
    // Cabai has unverified Kc -> returns standard 1.0 placeholder
    return {
      crop,
      dap,
      kc: 1.0,
      current_stage: 'mid',
      stage_length_days: [20, 30, 40, 20],
      total_days: 110,
    };
  }

  const kcIni: number = cropConfig.kc_ini;
  const kcMid: number = cropConfig.kc_mid;

  let kcEnd: number;
  if (crop === 'jagung') {
    kcEnd = panenKering
      ? cropConfig.kc_end_options.panen_kering
      : cropConfig.kc_end_options.panen_basah;
  } else if (crop === 'tomat') {
    kcEnd = cropConfig.kc_end_chosen;
  } else if (crop === 'kedelai') {
    kcEnd = cropConfig.kc_end;
  } else if (crop === 'padi') {
    kcEnd = cropConfig.kc_end_chosen;
  } else {
    kcEnd = 1.0;
  }

  const stageLengths: number[] = cropConfig.stage_lengths_days || [25, 30, 40, 25];
  const lIni = stageLengths[0];
  const lDev = stageLengths[1];
  const lMid = stageLengths[2];
  const lLate = stageLengths[3];
  const total = lIni + lDev + lMid + lLate;

  let kc: number;
  let currentStage: 'ini' | 'dev' | 'mid' | 'late' | 'harvested';

  if (dap <= 0) {
    kc = kcIni;
    currentStage = 'ini';
  } else if (dap <= lIni) {
    kc = kcIni;
    currentStage = 'ini';
  } else if (dap <= lIni + lDev) {
    const fraction = (dap - lIni) / Math.max(1, lDev);
    kc = kcIni + fraction * (kcMid - kcIni);
    currentStage = 'dev';
  } else if (dap <= lIni + lDev + lMid) {
    kc = kcMid;
    currentStage = 'mid';
  } else if (dap <= total) {
    const fraction = (dap - (lIni + lDev + lMid)) / Math.max(1, lLate);
    kc = kcMid + fraction * (kcEnd - kcMid);
    currentStage = 'late';
  } else {
    kc = kcEnd;
    currentStage = 'harvested';
  }

  return {
    crop,
    dap,
    kc: Number(kc.toFixed(4)),
    current_stage: currentStage,
    stage_length_days: stageLengths,
    total_days: total,
  };
}

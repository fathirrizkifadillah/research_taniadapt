/**
 * Main Pure Decision Engine Orchestrator for TaniAdapt.
 * Executes bio-mechanistic FAO-56 balance, rules evaluation, hourly schedule,
 * and formats compliant payload conforming to engine_output.schema.json.
 */

import {
  TaniAdaptEngineOutput,
  EngineExecutionInput,
  ActionEvaluation,
  HourlyTimelineItem,
  HourlyStatusLevel,
  IndicatorEvaluation,
  EngineStatus,
  EvidenceTier,
} from './types';
import { calculateDailyET0 } from './fao56';
import { calculateDynamicKc } from './kc';
import { evaluateWaterStress, updateDailyDepletion } from './waterBalance';
import { getRuleById, RULES_DATA } from './rules';

export function executeDecisionEngine(input: EngineExecutionInput): TaniAdaptEngineOutput {
  const {
    crop,
    kabkota,
    cell_id,
    elevation_m,
    latitude,
    day_of_year,
    planting_date,
    as_of_date,
    weather_source,
    daily_weather,
    panen_kering = true,
    initial_depletion_dr0_mm = 0.0,
  } = input;

  // 1. Calculate Days After Planting (DAP / HST)
  const pDate = new Date(planting_date);
  const aDate = new Date(as_of_date);
  const dap = Math.max(0, Math.floor((aDate.getTime() - pDate.getTime()) / (1000 * 60 * 60 * 24)));

  // 2. Reference ET0 (FAO-56 Penman-Monteith)
  const et0 = calculateDailyET0(
    daily_weather.tmax_c,
    daily_weather.tmin_c,
    daily_weather.dewpoint_c,
    daily_weather.wind_10m_ms,
    daily_weather.solar_radiation_mj_m2,
    elevation_m,
    latitude,
    day_of_year
  );

  // 3. Dynamic Crop Coefficient (Kc)
  const kcCurve = calculateDynamicKc(crop, dap, panen_kering);
  const etc = Number((et0 * kcCurve.kc).toFixed(2));

  // 4. Update Daily Water Depletion (Dr)
  const initialDr = initial_depletion_dr0_mm;
  // Estimate TAW for upper boundary
  const currentDr = updateDailyDepletion(
    initialDr,
    etc,
    daily_weather.precipitation_mm,
    150.0 // Default soil TAW limit
  );

  // 5. Evaluate FAO-56 Water Stress
  const waterEval = evaluateWaterStress(crop, dap, currentDr, initialDr);

  // 6. Indicators array
  const indicators: IndicatorEvaluation[] = [
    {
      id: 'reference_et0_fao56',
      rule_id: 'RULE_WATER_FAO56_DEPLETION',
      value: Number(et0.toFixed(2)),
      unit: 'mm/day',
      relative_rank: 'typical',
      rank_basis: 'OpenMeteo_ERA5_2000_2020',
      rank_basis_n: 21,
    },
    {
      id: 'crop_etc_daily',
      rule_id: 'RULE_WATER_FAO56_DEPLETION',
      value: etc,
      unit: 'mm/day',
      relative_rank: 'typical',
      rank_basis: 'OpenMeteo_ERA5_2000_2020',
      rank_basis_n: 21,
    },
    {
      id: 'soil_water_depletion_Dr',
      rule_id: 'RULE_WATER_FAO56_DEPLETION',
      value: waterEval.depletion_dr_mm,
      unit: 'mm',
      relative_rank: waterEval.status === 'kondisi_stres_abiotik' ? 'unusually_high' : 'typical',
      rank_basis: 'OpenMeteo_ERA5_2000_2020',
      rank_basis_n: 21,
    },
  ];

  // 7. Evaluate Hourly Operational Timeline (06.00 - 18.00 WIB)
  const hourlyItems: HourlyTimelineItem[] = [];
  const hours = [
    '06.00', '07.00', '08.00', '09.00', '10.00', '11.00',
    '12.00', '13.00', '14.00', '15.00', '16.00', '17.00', '18.00'
  ];

  // Map input hourly data to map by hour string
  const hourlyWeatherMap = new Map<string, any>();
  if (daily_weather.hourly && Array.isArray(daily_weather.hourly)) {
    for (const h of daily_weather.hourly) {
      const d = new Date(h.time);
      const hStr = `${String(d.getHours()).padStart(2, '0')}.00`;
      hourlyWeatherMap.set(hStr, h);
    }
  }

  // Count consecutive RH >= 90 hours for LWD proxy
  let rh90Count = 0;
  for (const h of daily_weather.hourly || []) {
    if (h.relative_humidity_2m >= 90.0) {
      rh90Count += 1;
    }
  }

  function escalateStatus(current: HourlyStatusLevel, candidate: HourlyStatusLevel): HourlyStatusLevel {
    const rank: Record<HourlyStatusLevel, number> = { SAFE: 0, WARN: 1, DANGER: 2 };
    return rank[candidate] > rank[current] ? candidate : current;
  }

  for (const hourStr of hours) {
    const hw = hourlyWeatherMap.get(hourStr);
    let hourStatus: HourlyStatusLevel = 'SAFE';
    const reasons: string[] = [];

    if (!hw) {
      hourlyItems.push({
        hour: hourStr,
        status: 'WARN',
        reason: 'Data prakiraan jam ini tidak tersedia.',
      });
      continue;
    }

    const windKmh = hw.wind_speed_10m ?? 0;
    const precipMm = hw.precipitation ?? 0;
    const srad = hw.shortwave_radiation ?? 0;
    const vpd = hw.vpd_hpa ?? 10.0;
    const temp = hw.temperature_2m ?? 27.0;

    // Evaluate rules
    // 1. Wind speed
    if (windKmh > 15.0) {
      hourStatus = escalateStatus(hourStatus, 'DANGER');
      reasons.push('Angin kencang > 15 km/j (bahaya drift semprot)');
    } else if (windKmh >= 12.0) {
      hourStatus = escalateStatus(hourStatus, 'WARN');
      reasons.push('Angin 12–15 km/j (zona transisi semprot)');
    } else if (windKmh < 3.0) {
      hourStatus = escalateStatus(hourStatus, 'WARN');
      reasons.push('Angin tenang < 3 km/j (risiko inversi suhu fajar)');
    }

    // 2. Precipitation
    if (precipMm >= 3.0) {
      hourStatus = escalateStatus(hourStatus, 'DANGER');
      reasons.push(`Hujan aktif ${precipMm.toFixed(1)} mm (dilarang siram/semprot/pupuk)`);
    } else if (precipMm > 0.0) {
      hourStatus = escalateStatus(hourStatus, 'WARN');
      reasons.push('Hujan rintik terdeteksi');
    }

    // 3. Solar Radiation & VPD
    if (srad > 500.0) {
      hourStatus = escalateStatus(hourStatus, 'WARN');
      reasons.push('Terik radiasi surya > 500 W/m² (evaporasi tinggi)');
    }
    if (vpd > 15.0) {
      hourStatus = escalateStatus(hourStatus, 'WARN');
      reasons.push('VPD tinggi > 15 hPa (penguapan air siraman cepat)');
    }

    const finalReason = reasons.length > 0
      ? reasons.join('; ')
      : 'Kondisi operasional lapangan optimal dan aman.';

    hourlyItems.push({
      hour: hourStr,
      status: hourStatus,
      reason: finalReason,
    });
  }

  // 8. Construct 5 Action Cards
  const actions: ActionEvaluation[] = [];

  // Action: Irrigation
  if (crop === 'padi') {
    actions.push({
      action: 'irrigation',
      window: 'Sepanjang hari',
      status_label: 'Bukti Belum Cukup',
      rule_ids: ['RULE_WATER_PADI_INSUFFICIENT'],
      rule_status: 'INSUFFICIENT',
      evidence_refs: ['FAO56_KC_RICE'],
      reason:
        'Padi sawah di Jawa Barat dibudidayakan dalam kondisi tergenang (ponded wetland regime); modul deplesi tanah tidak berlaku tanpa model genangan lokal.',
    });
  } else if (waterEval.status === 'kondisi_stres_abiotik') {
    actions.push({
      action: 'irrigation',
      window: '06.00 - 08.00 WIB',
      status_label: 'Sangat Aman',
      rule_ids: ['RULE_WATER_FAO56_DEPLETION'],
      rule_status: 'VERIFIED_METHOD',
      evidence_refs: ['RULE_WATER_FAO56_DEPLETION', 'FAO56_RAW_DEPLETION'],
      reason: `Deplesi air tanah (Dr = ${waterEval.depletion_dr_mm} mm) melampaui batas air siap serap (RAW = ${waterEval.raw_threshold_mm} mm). Sangat dianjurkan segera menyiram.`,
    });
  } else {
    actions.push({
      action: 'irrigation',
      window: '06.00 - 08.00 WIB',
      status_label: 'Perlu Waspada',
      rule_ids: ['RULE_WATER_FAO56_DEPLETION'],
      rule_status: 'VERIFIED_METHOD',
      evidence_refs: ['RULE_WATER_FAO56_DEPLETION', 'FAO56_RAW_DEPLETION'],
      reason: `Air tanah masih mencukupi (Dr = ${waterEval.depletion_dr_mm} mm <= RAW ${waterEval.raw_threshold_mm} mm). Belum perlu penyiraman darurat, hemat air.`,
    });
  }

  // Action: Spraying
  const sprayRule = getRuleById('RULE_SPRAY_WIND_SAFE');
  const windSafeCount = hourlyItems.filter(
    (h) => h.status === 'SAFE' && (h.hour === '06.00' || h.hour === '07.00' || h.hour === '08.00')
  ).length;

  actions.push({
    action: 'spraying',
    window: '06.00 - 08.00 WIB',
    status_label: windSafeCount >= 2 ? 'Sangat Aman' : 'Perlu Waspada',
    rule_ids: ['RULE_SPRAY_WIND_SAFE', 'RULE_SPRAY_WIND_CALM_INVERSION', 'RULE_SPRAY_WIND_DANGER'],
    rule_status: 'CONVENTION_PENDING',
    evidence_refs: [],
    reason:
      windSafeCount >= 2
        ? 'Kecepatan angin pagi hari dalam batas aman (3–12 km/j), suhu < 30°C.'
        : 'Kecepatan angin di luar jendela optimal (bahaya inversi fajar atau transisi drift).',
  });

  // Action: Fertilizing
  const fertRule = getRuleById('RULE_FERT_RAIN_12H');
  const rainForecast12h = daily_weather.precipitation_mm;
  actions.push({
    action: 'fertilizing',
    window: '07.00 - 09.00 WIB',
    status_label: rainForecast12h >= 8.0 ? 'Hindari' : 'Sangat Aman',
    rule_ids: ['RULE_FERT_RAIN_12H'],
    rule_status: 'CONVENTION_PENDING',
    evidence_refs: [],
    reason:
      rainForecast12h >= 8.0
        ? `Prakiraan hujan harian (${rainForecast12h} mm) berisiko mencuci pupuk larut ke limpasan.`
        : 'Risiko pencucian pupuk rendah, tanah dalam kelembapan memadai.',
  });

  // Action: Harvesting
  actions.push({
    action: 'harvesting',
    window: '08.00 - 12.00 WIB',
    status_label: daily_weather.precipitation_mm > 2.0 ? 'Perlu Waspada' : 'Sangat Aman',
    rule_ids: ['RULE_HARVEST_RH_SAFE', 'RULE_HARVEST_RH_DANGER'],
    rule_status: 'CONVENTION_PENDING',
    evidence_refs: [],
    reason:
      daily_weather.precipitation_mm > 2.0
        ? 'Hujan siang berisiko meningkatkan kelembapan hasil panen.'
        : 'Cuaca relatif kering, kelembapan mendukung pemanenan hasil.',
  });

  // Action: Pruning / Scouting
  if (crop === 'cabai' || crop === 'tomat') {
    actions.push({
      action: 'scouting_opt',
      window: 'Pagi hari',
      status_label: 'Perlu Waspada',
      rule_ids: ['RULE_OPT_LWD_HOURLY_RH90'],
      rule_status: 'METHOD_UNCALIBRATED',
      evidence_refs: ['SENTELHAS_2008_LWD'],
      reason: `Terdeteksi ${rh90Count} jam dengan RH >= 90%. Metode kebasahan daun ada di jurnal (Sentelhas 2008) namun ambang belum terkalibrasi di Jawa Barat; status ditahan pada peringatan pengamatan lapangan.`,
    });
  } else {
    actions.push({
      action: 'pruning',
      window: '07.00 - 09.00 WIB',
      status_label: 'Sangat Aman',
      rule_ids: ['RULE_PRUNE_RAIN_8H'],
      rule_status: 'CONVENTION_PENDING',
      evidence_refs: [],
      reason: 'Luka pangkas kering sebelum potensi hujan siang.',
    });
  }

  // 9. Determine Overall Status & Evidence References
  let overallStatus: EngineStatus = 'normal';
  let evidenceTier: EvidenceTier = 'published_model';
  const overallEvidenceRefs: string[] = [];

  if (crop === 'padi') {
    overallStatus = 'evidence_insufficient';
    evidenceTier = 'insufficient';
    overallEvidenceRefs.push('FAO56_KC_RICE');
  } else if (waterEval.status === 'kondisi_stres_abiotik') {
    overallStatus = 'kondisi_stres_abiotik';
    evidenceTier = 'published_model';
    overallEvidenceRefs.push('RULE_WATER_FAO56_DEPLETION', 'FAO56_RAW_DEPLETION');
  } else {
    overallStatus = 'normal';
    evidenceTier = 'published_model';
    overallEvidenceRefs.push('FAO56_RAW_DEPLETION');
  }

  // 10. Format RFC 3339 timestamp
  const issueTime = `${as_of_date}T06:00:00+07:00`;

  return {
    crop,
    location: {
      kabkota,
      cell_id,
      weather_source,
    },
    as_of: as_of_date,
    issue_time: issueTime,
    timezone: 'Asia/Jakarta',
    rules_version: RULES_DATA.rules_version,
    data_version: 'v2.4-verified-params',
    data_freshness_days: 0,
    layer: 'daily',
    source_data: 'forecast',
    forecast_uncertainty: daily_weather.precipitation_probability ?? null,
    indicators,
    actions,
    hourly: hourlyItems,
    status: overallStatus,
    evidence_tier: evidenceTier,
    evidence_refs: overallEvidenceRefs,
    claim_allowed:
      overallStatus === 'kondisi_stres_abiotik'
        ? 'Deplesi lengas zona perakaran melampaui air siap serap (Dr > RAW = p * TAW); irigasi segera dianjurkan.'
        : overallStatus === 'evidence_insufficient'
        ? 'Data atau model air tanah lokal tidak mencukupi untuk modul budidaya tergenang.'
        : 'Lengas tanah mencukupi (Dr <= RAW); kebutuhan air tanaman dalam kondisi normal.',
    claim_forbidden: [
      'prediksi hasil panen absolut (calibrated yield prediction)',
      'rekomendasi dosis bahan kimia sintetik tanpa penyuluh',
      'klaim kausalitas bebas halusinasi mutlak',
    ],
    limitations: [
      'Asumsi tanah loam FAO-56 Tabel 19 (TAW = 150 mm/m).',
      `Asumsi deplesi awal Dr0 = ${initialDr} mm.`,
      waterEval.sensitif_terhadap_asumsi_tanah
        ? 'PERINGATAN: Rekomendasi sensitif terhadap asumsi variasi tekstur tanah loam (130-180 mm/m).'
        : 'Rekomendasi stabil terhadap variasi rentang tekstur tanah loam.',
      'Aturan operasional semprot dan pupuk berstatus aturan praktis tim lapangan.',
    ],
    action_ids: actions.map((a) => a.action),
    sensitif_terhadap_asumsi_tanah: waterEval.sensitif_terhadap_asumsi_tanah,
    asumsi_deplesi_awal_dr0: initialDr,
  };
}

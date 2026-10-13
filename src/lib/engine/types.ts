/**
 * Type definitions for TaniAdapt Decision Engine.
 * Strictly conforms to schemas/engine_output.schema.json (Draft 2020-12).
 */

export type CropType = 'padi' | 'jagung' | 'kedelai' | 'cabai' | 'tomat';

export type EngineStatus =
  | 'normal'
  | 'kondisi_mendukung_OPT'
  | 'kondisi_stres_abiotik'
  | 'evidence_insufficient';

export type RuleStatus =
  | 'VERIFIED_METHOD'
  | 'METHOD_UNCALIBRATED'
  | 'CONVENTION_PENDING'
  | 'INSUFFICIENT'
  | 'DEPRECATED';

export type HourlyStatusLevel = 'SAFE' | 'WARN' | 'DANGER';

export type EvidenceTier =
  | 'data_learned'
  | 'published_model'
  | 'literature_transfer'
  | 'convention_pending'
  | 'insufficient';

export type WeatherSource =
  | 'AgERA5_CDS'
  | 'OpenMeteo_ERA5'
  | 'BMKG_Station'
  | 'Synthetic_Test';

export interface LocationInfo {
  kabkota: string;
  cell_id: string;
  weather_source: string;
}

export interface IndicatorEvaluation {
  id: string;
  rule_id: string;
  value: number | null;
  unit: string;
  relative_rank: 'low' | 'typical' | 'unusually_high' | null;
  rank_basis: string | null;
  rank_basis_n: number | null;
}

export interface ActionEvaluation {
  action: 'irrigation' | 'spraying' | 'fertilizing' | 'harvesting' | 'pruning' | 'drainage_inspection' | 'scouting_opt';
  window: string;
  status_label: 'Sangat Aman' | 'Perlu Waspada' | 'Hindari' | 'Bukti Belum Cukup';
  rule_ids: string[];
  rule_status: RuleStatus;
  evidence_refs: string[];
  reason: string;
}

export interface HourlyTimelineItem {
  hour: string; // e.g. "06.00"
  status: HourlyStatusLevel;
  reason: string;
}

export interface TaniAdaptEngineOutput {
  crop: CropType;
  location: LocationInfo;
  as_of: string; // YYYY-MM-DD
  issue_time: string; // ISO 8601 date-time RFC 3339
  timezone: 'Asia/Jakarta';
  rules_version: string;
  data_version: string;
  data_freshness_days: number | null;
  layer: 'seasonal' | 'daily' | 'hourly';
  source_data: 'forecast' | 'reanalysis' | 'reanalysis_forecast' | 'station' | null;
  forecast_uncertainty?: number | null;
  indicators: IndicatorEvaluation[];
  actions: ActionEvaluation[];
  hourly: HourlyTimelineItem[];
  status: EngineStatus;
  evidence_tier: EvidenceTier;
  evidence_refs: string[];
  claim_allowed: string;
  claim_forbidden: string[];
  limitations: string[];
  action_ids: string[];
  // Metadata flags
  sensitif_terhadap_asumsi_tanah?: boolean;
  asumsi_deplesi_awal_dr0?: number;
}

export interface HourlyWeatherData {
  time: string; // ISO timestamp
  temperature_2m: number;
  relative_humidity_2m: number;
  dewpoint_2m?: number;
  precipitation: number;
  precipitation_probability?: number;
  wind_speed_10m: number; // km/h
  shortwave_radiation: number; // W/m2
  vpd_hpa?: number;
}

export interface DailyWeatherSummary {
  date: string;
  tmax_c: number;
  tmin_c: number;
  dewpoint_c: number;
  wind_10m_ms: number;
  solar_radiation_mj_m2: number;
  precipitation_mm: number;
  precipitation_probability?: number;
  hourly: HourlyWeatherData[];
}

export interface EngineExecutionInput {
  crop: CropType;
  kabkota: string;
  cell_id: string;
  elevation_m: number;
  latitude: number;
  day_of_year: number;
  planting_date: string; // YYYY-MM-DD
  as_of_date: string; // YYYY-MM-DD
  weather_source: WeatherSource;
  climatology_source?: WeatherSource;
  daily_weather: DailyWeatherSummary;
  soil_texture?: 'sand' | 'sandy_loam' | 'loam' | 'clay_loam' | 'clay';
  panen_kering?: boolean; // For maize Kc_end
  initial_depletion_dr0_mm?: number; // Explicit Dr0 input
}

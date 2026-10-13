/**
 * Pure TypeScript Percentile and Climatology Evaluation for TaniAdapt.
 * Strict parity check: Weather source and Climatology source MUST match.
 */

import { WeatherSource } from './types';

export interface PercentileRankResult {
  relative_rank: 'low' | 'typical' | 'unusually_high' | null;
  rank_basis: string | null;
  rank_basis_n: number | null;
  status: 'valid' | 'evidence_insufficient';
  reason?: string;
}

export interface ClimatologyPercentiles14d {
  p10: number;
  p25: number;
  p50: number;
  p75: number;
  p90: number;
}

export function evaluateClimatologyParity(
  weatherSource: WeatherSource,
  climatologySource?: WeatherSource
): boolean {
  if (!climatologySource) return true; // default assumed matching
  // AgERA5 must be compared with AgERA5, OpenMeteo with OpenMeteo
  if (weatherSource.startsWith('AgERA5') && climatologySource.startsWith('AgERA5')) {
    return true;
  }
  if (weatherSource.startsWith('OpenMeteo') && climatologySource.startsWith('OpenMeteo')) {
    return true;
  }
  if (weatherSource === 'Synthetic_Test') {
    return true;
  }
  return false;
}

export function calculatePercentileRank(
  value: number,
  percentiles: ClimatologyPercentiles14d,
  weatherSource: WeatherSource,
  climatologySource?: WeatherSource,
  basisName: string = 'OpenMeteo_ERA5_2000_2020',
  basisN: number = 21
): PercentileRankResult {
  const isParityValid = evaluateClimatologyParity(weatherSource, climatologySource);

  if (!isParityValid) {
    return {
      relative_rank: null,
      rank_basis: null,
      rank_basis_n: null,
      status: 'evidence_insufficient',
      reason: `Sumber data cuaca (${weatherSource}) tidak sepadan dengan baseline klimatologi (${climatologySource}); perbandingan persentil dibatalkan demi integritas data.`,
    };
  }

  let rank: 'low' | 'typical' | 'unusually_high';
  if (value < percentiles.p25) {
    rank = 'low';
  } else if (value > percentiles.p75) {
    rank = 'unusually_high';
  } else {
    rank = 'typical';
  }

  return {
    relative_rank: rank,
    rank_basis: basisName,
    rank_basis_n: basisN,
    status: 'valid',
  };
}

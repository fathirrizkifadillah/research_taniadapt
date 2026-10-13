"""FAO-56 daily reference-ET, crop coefficient, and root zone water depletion helpers.

Input units: Celsius, kPa, MJ m-2 day-1, metres, and m s-1. The equations
follow FAO-56 (Allen et al., 1998):
- Eq. 6 (p. 65): FAO-56 Penman-Monteith reference evapotranspiration (ET0).
- Table 11 (pp. 104-108): Lengths of crop development stages (days).
- Table 12 (pp. 109-114): Single crop coefficients (Kc_ini, Kc_mid, Kc_end).
- Table 19 (p. 165): Available soil water capacity (TAW) and moisture limits (theta_FC, theta_WP).
- Table 22 (pp. 167-168): Maximum rooting depth (Zr) and depletion fraction for no stress (p).
"""
from __future__ import annotations

import math
from datetime import date, datetime
from typing import Dict, Any, Optional


def wind_2m(wind_10m: float) -> float:
    """Convert 10 m wind speed to 2 m using FAO-56 Eq. 47."""
    return wind_10m * 4.87 / math.log(67.8 * 10.0 - 5.42)


def saturation_vp(temp_c: float) -> float:
    return 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))


def delta_svp(temp_c: float) -> float:
    es = saturation_vp(temp_c)
    return 4098.0 * es / ((temp_c + 237.3) ** 2)


def pressure_kpa(elevation_m: float) -> float:
    return 101.3 * ((293.0 - 0.0065 * elevation_m) / 293.0) ** 5.26


def extraterrestrial_radiation(latitude_deg: float, day_of_year: int) -> float:
    phi = math.radians(latitude_deg)
    dr = 1.0 + 0.033 * math.cos(2.0 * math.pi * day_of_year / 365.0)
    solar_declination = 0.409 * math.sin(2.0 * math.pi * day_of_year / 365.0 - 1.39)
    sunset_angle = math.acos(max(-1.0, min(1.0, -math.tan(phi) * math.tan(solar_declination))))
    return (24.0 * 60.0 / math.pi) * 0.0820 * dr * (
        sunset_angle * math.sin(phi) * math.sin(solar_declination)
        + math.cos(phi) * math.cos(solar_declination) * math.sin(sunset_angle)
    )


def daily_et0(tmax_c: float, tmin_c: float, dewpoint_c: float, wind_10m_ms: float,
              solar_radiation_mj_m2_day: float, elevation_m: float,
              latitude_deg: float, day_of_year: int) -> float:
    """Daily FAO-56 PM ET0 (Eq. 6, p. 65); daily soil heat flux G = 0 (Eq. 42)."""
    tmean = (tmax_c + tmin_c) / 2.0
    es = (saturation_vp(tmax_c) + saturation_vp(tmin_c)) / 2.0
    ea = saturation_vp(dewpoint_c)
    delta = delta_svp(tmean)
    gamma = 0.000665 * pressure_kpa(elevation_m)
    u2 = wind_2m(wind_10m_ms)
    ra = extraterrestrial_radiation(latitude_deg, day_of_year)
    rso = (0.75 + 2e-5 * elevation_m) * ra
    rs = max(0.0, solar_radiation_mj_m2_day)
    rns = 0.77 * rs
    sigma = 4.903e-9
    rnl = sigma * (((tmax_c + 273.16) ** 4 + (tmin_c + 273.16) ** 4) / 2.0) * (
        0.34 - 0.14 * math.sqrt(max(ea, 0.0))
    ) * (1.35 * min(rs / rso, 1.0) - 0.35)
    rn = rns - rnl
    numerator = 0.408 * delta * rn + gamma * (900.0 / (tmean + 273.0)) * u2 * max(es - ea, 0.0)
    denominator = delta + gamma * (1.0 + 0.34 * u2)
    return max(0.0, numerator / denominator)


def validate_fao56_example18() -> float:
    """Reproduce FAO-56 Example 18 (Uccle): expected ET0 ~3.88 mm/day."""
    delta, gamma, u2, es, ea, rn = 0.122, 0.0666, 2.078, 1.997, 1.409, 13.28
    benchmark = (0.408 * delta * rn + gamma * (900.0 / (16.9 + 273.0)) * u2 * (es - ea)) / (
        delta + gamma * (1.0 + 0.34 * u2)
    )
    if abs(benchmark - 3.88) > 0.03:
        raise AssertionError(f"FAO-56 Example 18 mismatch: {benchmark:.3f}")
    return benchmark


# --- FAO-56 TABLES & SOIL WATER BALANCE ---

# Typical soil water capacities from FAO-56 Table 19 (p. 165)
SOIL_TEXTURE_TABLE19: Dict[str, Dict[str, float]] = {
    "sand": {"theta_fc": 0.12, "theta_wp": 0.05, "taw_mm_m": 70.0},
    "sandy_loam": {"theta_fc": 0.23, "theta_wp": 0.10, "taw_mm_m": 130.0},
    "loam": {"theta_fc": 0.27, "theta_wp": 0.12, "taw_mm_m": 150.0},
    "clay_loam": {"theta_fc": 0.32, "theta_wp": 0.18, "taw_mm_m": 140.0},
    "clay": {"theta_fc": 0.38, "theta_wp": 0.24, "taw_mm_m": 140.0},
}

# Crop development stage lengths from FAO-56 Table 11 (pp. 104-108)
CROP_STAGES_TABLE11: Dict[str, Dict[str, int]] = {
    "jagung": {"ini": 20, "dev": 35, "mid": 40, "late": 30, "total": 125}, # Table 11 p. 103: Nigeria (humid)
    "kedelai": {"ini": 15, "dev": 15, "mid": 40, "late": 15, "total": 85},  # Table 11 p. 104: Tropics
    "tomat": {"ini": 30, "dev": 40, "mid": 45, "late": 30, "total": 145},
    "padi": {"ini": 30, "dev": 30, "mid": 35, "late": 25, "total": 120},
}

# Crop coefficients and rooting parameters from FAO-56 Table 12 & Table 22
CROP_PARAMS_TABLE12_22: Dict[str, Dict[str, Any]] = {
    "jagung": {
        "kc_ini": 0.30, "kc_mid": 1.20, "kc_end": 0.35, "kc_end_range": [0.60, 0.35], # Table 12 p. 110: 0.60 (panen basah) s.d. 0.35 (panen kering di batang)
        "kc_end_harvest_assumption": "0.35 (asumsi panen kering di batang; 0.60 jika panen biji berkadar air tinggi)",
        "zr_min": 0.3, "zr_max": 1.0, "p": 0.55,       # Table 22 p. 167 (zr_chosen = 1.0)
        "evidence_id_kc": "FAO56_KC_MAIZE",
        "evidence_id_water": "FAO56_RAW_DEPLETION",
        "water_module_status": "VERIFIED"
    },
    "kedelai": {
        "kc_ini": 0.40, "kc_mid": 1.15, "kc_end": 0.50, "kc_end_range": [0.50, 0.50], # Table 12 p. 110: nilai tunggal definitif
        "kc_end_harvest_assumption": "0.50 (kondisi panen polong kering standar)",
        "zr_min": 0.3, "zr_max": 0.8, "p": 0.50,       # Table 22 p. 167 (zr_chosen = 0.8)
        "evidence_id_kc": "FAO56_KC_SOY",
        "evidence_id_water": "FAO56_RAW_DEPLETION",
        "water_module_status": "VERIFIED"
    },
    "tomat": {
        "kc_ini": 0.60, "kc_mid": 1.15, "kc_end": 0.80, "kc_end_range": [0.70, 0.90], # Table 12 p. 110: 0.70-0.80 processing; 0.80-0.90 fresh
        "kc_end_harvest_assumption": "0.80 (asumsi tomat konsumsi segar; 0.70 jika tomat olahan)",
        "zr_min": 0.25, "zr_max": 0.7, "p": 0.40,      # Table 22 p. 167 (zr_chosen = 0.7)
        "evidence_id_kc": "FAO56_KC_TOMATO",
        "evidence_id_water": "FAO56_RAW_DEPLETION",
        "water_module_status": "VERIFIED"
    },
    "padi": {
        "kc_ini": 1.05, "kc_mid": 1.20, "kc_end": 0.60, "kc_end_range": [0.90, 0.60], # Table 12 p. 110: 0.90 air tergenang; 0.60 dikeringkan pra-panen
        "kc_end_harvest_assumption": "0.60 (asumsi sawah dikeringkan 2-3 minggu pra-panen; 0.90 jika sawah masih tergenang)",
        "zr_min": 0.5, "zr_max": 1.0, "p": 0.20,       # Table 22 p. 167
        "evidence_id_kc": "FAO56_KC_RICE",
        "evidence_id_water": None,
        "water_module_status": "evidence_insufficient",
        "insufficient_reason": "Kc padi sawah FAO-56 Tabel 12 mengasumsikan sawah tergenang (ponded water layer); modul deplesi tanah tidak berlaku tanpa model perkolasi genangan lokal."
    },
    "cabai": {
        "kc_ini": None, "kc_mid": None, "kc_end": None,
        "zr_min": 0.3, "zr_max": 0.8, "p": 0.30,
        "evidence_id_kc": "CHILI_WATER (UNVERIFIED)",
        "evidence_id_water": None,
        "water_module_status": "evidence_insufficient",
        "insufficient_reason": "Koefisien Kc cabai tropis belum terverifikasi di evidence registry (sweet pepper tidak diekstrapolasi)."
    }
}


def calculate_dynamic_kc(crop: str, dap: int) -> float:
    """Calculate daily Kc based on Days After Planting (DAP/HST) and FAO-56 Table 11 & 12."""
    if crop not in CROP_STAGES_TABLE11 or crop not in CROP_PARAMS_TABLE12_22:
        return 1.0
    
    stages = CROP_STAGES_TABLE11[crop]
    params = CROP_PARAMS_TABLE12_22[crop]
    kc_ini = params.get("kc_ini")
    kc_mid = params.get("kc_mid")
    kc_end = params.get("kc_end")
    if kc_ini is None or kc_mid is None or kc_end is None:
        return 1.0
    
    l_ini = stages["ini"]
    l_dev = stages["dev"]
    l_mid = stages["mid"]
    l_late = stages["late"]
    total = stages["total"]

    if dap <= l_ini:
        return kc_ini
    elif dap <= l_ini + l_dev:
        frac = (dap - l_ini) / max(1, l_dev)
        return kc_ini + frac * (kc_mid - kc_ini)
    elif dap <= l_ini + l_dev + l_mid:
        return kc_mid
    elif dap <= total:
        frac = (dap - (l_ini + l_dev + l_mid)) / max(1, l_late)
        return kc_mid + frac * (kc_end - kc_mid)
    else:
        return kc_end


def calculate_root_depth(crop: str, dap: int) -> float:
    """Estimate effective root depth Zr at given DAP (HST) between Zr_min and Zr_max."""
    params = CROP_PARAMS_TABLE12_22.get(crop, {})
    zr_min = params.get("zr_min", 0.3)
    zr_max = params.get("zr_max", 1.0)
    stages = CROP_STAGES_TABLE11.get(crop, {"ini": 20, "dev": 30, "total": 100})
    l_root_max = stages.get("ini", 20) + stages.get("dev", 30)
    if dap <= 0:
        return zr_min
    elif dap >= l_root_max:
        return zr_max
    else:
        return zr_min + (dap / l_root_max) * (zr_max - zr_min)


def calculate_taw_raw(crop: str, dap: int, soil_type: str = "loam") -> Dict[str, Any]:
    """Calculate Total Available Water (TAW) and Readily Available Water (RAW = p * TAW).
    
    References:
    - TAW = 1000 * (theta_FC - theta_WP) * Zr (FAO-56 Eq. 82, p. 162; Table 19 p. 165).
    - RAW = p * TAW (FAO-56 Eq. 83, p. 162; Table 22 pp. 167-168).
    """
    soil = SOIL_TEXTURE_TABLE19.get(soil_type, SOIL_TEXTURE_TABLE19["loam"])
    zr = calculate_root_depth(crop, dap)
    taw = soil["taw_mm_m"] * zr # mm
    p_fraction = CROP_PARAMS_TABLE12_22.get(crop, {}).get("p", 0.50)
    raw = p_fraction * taw
    return {
        "root_depth_m": round(zr, 2),
        "taw_mm": round(taw, 2),
        "raw_mm": round(raw, 2),
        "p_fraction": p_fraction,
        "soil_type": soil_type
    }


def evaluate_fao56_water_stress(crop: str, dap: int, depletion_dr_mm: float, soil_type: str = "loam") -> Dict[str, Any]:
    """Evaluate whether root zone water depletion Dr exceeds RAW (FAO-56 Chapter 8)."""
    params = CROP_PARAMS_TABLE12_22.get(crop, {})
    if params.get("water_module_status") == "evidence_insufficient":
        return {
            "status": "evidence_insufficient",
            "evidence_tier": "insufficient",
            "reason": params.get("insufficient_reason", "Parameter air belum terverifikasi.")
        }
    
    water_params = calculate_taw_raw(crop, dap, soil_type)
    raw_mm = water_params["raw_mm"]
    taw_mm = water_params["taw_mm"]

    if depletion_dr_mm > raw_mm:
        stress_status = "kondisi_stres_abiotik"
        recommendation = "Irigasi replenishment segera diperlukan; deplesi melampaui batas air siap serap (Dr > RAW)."
    else:
        stress_status = "normal"
        recommendation = "Lengas tanah mencukupi (Dr <= RAW); tidak memerlukan irigasi darurat."
    
    return {
        "status": stress_status,
        "evidence_id": "FAO56_RAW_DEPLETION",
        "evidence_tier": "published_model",
        "depletion_dr_mm": round(depletion_dr_mm, 2),
        "raw_threshold_mm": raw_mm,
        "taw_mm": taw_mm,
        "recommendation": recommendation,
        "soil_type": soil_type,
        "dap": dap
    }

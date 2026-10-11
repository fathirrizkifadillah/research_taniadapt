import csv
import os

os.makedirs("reports/dataset_discovery", exist_ok=True)

# Exact list from Copernicus API schema
variables_info = [
    {
        "display_label": "Precipitation flux",
        "exact_identifier": "precipitation_flux",
        "statistic_if_required": "24_hour_total",
        "units_and_definition": "mm/day or kg m-2 s-1; Total precipitation amount accumulated over 24 hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Essential primary agroclimatic variable for irrigation, waterlogging risk, and fungal disease forecasting."
    },
    {
        "display_label": "2m temperature (24-hour mean)",
        "exact_identifier": "2m_temperature_24_hour_mean",
        "statistic_if_required": "24_hour_mean",
        "units_and_definition": "K or °C; Mean 2-meter air temperature over 24 hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Core thermal variable for thermal time (GDD), phenological development, and general crop growth."
    },
    {
        "display_label": "2m temperature (24-hour maximum)",
        "exact_identifier": "2m_temperature_24_hour_maximum",
        "statistic_if_required": "24_hour_maximum",
        "units_and_definition": "K or °C; Maximum 2-meter air temperature over 24 hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Critical for extreme heat stress detection, pollen sterility, and maximum diurnal temperature range."
    },
    {
        "display_label": "2m temperature (24-hour minimum)",
        "exact_identifier": "2m_temperature_24_hour_minimum",
        "statistic_if_required": "24_hour_minimum",
        "units_and_definition": "K or °C; Minimum 2-meter air temperature over 24 hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Critical for cold injury, night respiration, minimum diurnal range, and disease sporulation thresholds."
    },
    {
        "display_label": "2m temperature (Day-time maximum)",
        "exact_identifier": "2m_temperature_day_time_maximum",
        "statistic_if_required": "day_time_maximum",
        "units_and_definition": "K or °C; Maximum temperature during daylight hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Captures peak photosynthetic daytime thermal stress conditions."
    },
    {
        "display_label": "2m temperature (Day-time mean)",
        "exact_identifier": "2m_temperature_day_time_mean",
        "statistic_if_required": "day_time_mean",
        "units_and_definition": "K or °C; Mean temperature during daylight hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Captures daytime active metabolic temperature."
    },
    {
        "display_label": "2m temperature (Night-time mean)",
        "exact_identifier": "2m_temperature_night_time_mean",
        "statistic_if_required": "night_time_mean",
        "units_and_definition": "K or °C; Mean temperature during night hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Key for dark respiration rate, carbon loss in rice and tropical crops."
    },
    {
        "display_label": "2m temperature (Night-time minimum)",
        "exact_identifier": "2m_temperature_night_time_minimum",
        "statistic_if_required": "night_time_minimum",
        "units_and_definition": "K or °C; Minimum temperature during night hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Key for overnight dew formation and nocturnal disease germination."
    },
    {
        "display_label": "2m dewpoint temperature",
        "exact_identifier": "2m_dewpoint_temperature_24_hour_mean",
        "statistic_if_required": "24_hour_mean",
        "units_and_definition": "K or °C; Temperature to which air must be cooled to become saturated",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Essential proxy for absolute moisture content and leaf wetness duration."
    },
    {
        "display_label": "Derived 2m relative humidity (maximum)",
        "exact_identifier": "derived_2m_relative_humidity_24_hour_maximum",
        "statistic_if_required": "24_hour_maximum",
        "units_and_definition": "% (0-100); Daily maximum relative humidity derived from Tmin and dewpoint",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Core variable for nighttime/early morning fungal spore germination and disease risk."
    },
    {
        "display_label": "Derived 2m relative humidity (minimum)",
        "exact_identifier": "derived_2m_relative_humidity_24_hour_minimum",
        "statistic_if_required": "24_hour_minimum",
        "units_and_definition": "% (0-100); Daily minimum relative humidity derived from Tmax and dewpoint",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Key indicator of peak afternoon atmospheric drying and crop water stress."
    },
    {
        "display_label": "2m relative humidity at 06:00",
        "exact_identifier": "2m_relative_humidity_at_06_00",
        "statistic_if_required": "06_00_local",
        "units_and_definition": "% (0-100); Relative humidity at 06:00 local solar time",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Provides diurnal cycle sampling at dawn for dew duration assessment."
    },
    {
        "display_label": "2m relative humidity at 09:00",
        "exact_identifier": "2m_relative_humidity_at_09_00",
        "statistic_if_required": "09_00_local",
        "units_and_definition": "% (0-100); Relative humidity at 09:00 local solar time",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Provides diurnal morning transition sampling for field operations/spraying advisory."
    },
    {
        "display_label": "2m relative humidity at 12:00",
        "exact_identifier": "2m_relative_humidity_at_12_00",
        "statistic_if_required": "12_00_local",
        "units_and_definition": "% (0-100); Relative humidity at 12:00 local solar time",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Provides midday humidity measurement around peak solar irradiance."
    },
    {
        "display_label": "2m relative humidity at 15:00",
        "exact_identifier": "2m_relative_humidity_at_15_00",
        "statistic_if_required": "15_00_local",
        "units_and_definition": "% (0-100); Relative humidity at 15:00 local solar time",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Provides afternoon humidity measurement during maximum daily temperature window."
    },
    {
        "display_label": "2m relative humidity at 18:00",
        "exact_identifier": "2m_relative_humidity_at_18_00",
        "statistic_if_required": "18_00_local",
        "units_and_definition": "% (0-100); Relative humidity at 18:00 local solar time",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Provides evening humidity measurement at the start of nighttime moisture accumulation."
    },
    {
        "display_label": "Vapour pressure deficit at maximum temperature",
        "exact_identifier": "vapour_pressure_deficit_at_maximum_temperature",
        "statistic_if_required": "at_tmax",
        "units_and_definition": "hPa or kPa; Difference between saturation and actual vapour pressure at daily Tmax",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "High-value biophysical stress metric directly governing stomatal closure and transpiration."
    },
    {
        "display_label": "Vapour pressure (24-hour mean)",
        "exact_identifier": "vapour_pressure_24_hour_mean",
        "statistic_if_required": "24_hour_mean",
        "units_and_definition": "hPa; Mean actual water vapour pressure in air over 24 hours",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Atmospheric moisture variable required for microclimatic energy balance."
    },
    {
        "display_label": "Reference evapotranspiration (ET0)",
        "exact_identifier": "reference_evapotranspiration",
        "statistic_if_required": "24_hour_total",
        "units_and_definition": "mm/day; FAO-56 Penman-Monteith reference evapotranspiration",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Foundational variable for crop water requirement calculation and irrigation scheduling."
    },
    {
        "display_label": "Solar radiation flux",
        "exact_identifier": "solar_radiation_flux",
        "statistic_if_required": "24_hour_total",
        "units_and_definition": "J m-2 day-1 or W m-2; Downward surface solar radiation flux",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Primary energy driver for crop photosynthesis, biomass accumulation, and ET0."
    },
    {
        "display_label": "10m wind speed (24-hour mean)",
        "exact_identifier": "10m_wind_speed_24_hour_mean",
        "statistic_if_required": "24_hour_mean",
        "units_and_definition": "m/s; Mean 10-meter horizontal wind speed",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Influences canopy boundary layer resistance, spraying drift risk, and pathogen spore dispersal."
    },
    {
        "display_label": "Cloud cover (24-hour mean)",
        "exact_identifier": "cloud_cover_24_hour_mean",
        "statistic_if_required": "24_hour_mean",
        "units_and_definition": "fraction (0-1); Total cloud area fraction",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Informs sunshine duration, diffused vs direct light, and microclimatic canopy dampening."
    },
    {
        "display_label": "Precipitation duration fraction",
        "exact_identifier": "precipitation_duration_fraction",
        "statistic_if_required": "24_hour_fraction",
        "units_and_definition": "fraction (0-1); Proportion of 24h with precipitation >= 0.1 mm",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Differentiates short convective cloudbursts from prolonged drizzling rain, key for disease spore wash vs germination."
    },
    {
        "display_label": "Liquid precipitation duration fraction",
        "exact_identifier": "liquid_precipitation_duration_fraction",
        "statistic_if_required": "24_hour_fraction",
        "units_and_definition": "fraction (0-1); Proportion of 24h with liquid rainfall",
        "supported_status": "SUPPORTED",
        "decision": "INCLUDED",
        "rationale": "Specific liquid water duration for tropical canopies."
    },
    {
        "display_label": "Solid precipitation duration fraction",
        "exact_identifier": "solid_precipitation_duration_fraction",
        "statistic_if_required": "24_hour_fraction",
        "units_and_definition": "fraction (0-1); Proportion of 24h with snow/ice precipitation",
        "supported_status": "SUPPORTED",
        "decision": "EXCLUDED",
        "rationale": "Snow/freezing precipitation is non-existent in low-altitude tropical West Java agriculture."
    },
    {
        "display_label": "Snow thickness (24-hour mean)",
        "exact_identifier": "snow_thickness_24_hour_mean",
        "statistic_if_required": "24_hour_mean",
        "units_and_definition": "m; Mean snow depth",
        "supported_status": "SUPPORTED",
        "decision": "EXCLUDED",
        "rationale": "Physical snow depth is zero throughout Indonesian low-latitude agricultural study domain."
    },
    {
        "display_label": "Snow thickness LWE (24-hour mean)",
        "exact_identifier": "snow_thickness_lwe_24_hour_mean",
        "statistic_if_required": "24_hour_mean",
        "units_and_definition": "m; Liquid water equivalent of snow depth",
        "supported_status": "SUPPORTED",
        "decision": "EXCLUDED",
        "rationale": "Snow water equivalent is zero throughout tropical Indonesian agroclimatic zones."
    }
]

out_path = "reports/dataset_discovery/agera5_variable_inventory.csv"
fieldnames = ["display_label", "exact_identifier", "statistic_if_required", "units_and_definition", "supported_status", "decision", "rationale"]

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in variables_info:
        writer.writerow(row)

print(f"Created {out_path} with {len(variables_info)} variables cataloged.")

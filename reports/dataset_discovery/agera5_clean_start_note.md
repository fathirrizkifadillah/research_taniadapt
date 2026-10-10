# AgERA5 Clean-Start Acquisition Note

## Background
The previous AgERA5 raw downloads were intentionally deleted by the user to perform a complete, clean, and properly structured fresh-start data acquisition. This was a conscious user decision, not an agent failure or data-loss incident.

## Legacy State vs. New Architecture
- **Legacy approach:** The previous notebook (`01_AgERA5.ipynb`) configured the gridded product (`sis-agrometeorological-indicators`) split into 24 jobs across 47 individual annual requests (up to 1,128 requests), which resulted in large multi-gigabyte ZIP archives with individual NetCDF files for the bounding box.
- **New fresh architecture:** We verified and leveraged the official Copernicus AgERA5 time-series endpoint (`sis-agrometeorological-indicators-timeseries`). This endpoint:
  1. Accepts precise point/area proxies for the 7 target locations in West Java.
  2. Directly generates multi-variable combined CSV files.
  3. Returns daily time-series with unified variables (Kelvin temperatures, mm/day precipitation, relative humidity, solar radiation, VPD, and ET0).
  4. Reduces request complexity from 1,128 requests down to location-based batch requests with verifiable responses.

## Target Locations
1. **Tasikmalaya**: Administrative proxy (-7.33, 108.22)
2. **Bandung**: Administrative proxy (-6.91, 107.61)
3. **Bekasi**: Administrative proxy (-6.24, 107.00)
4. **Purwakarta**: Administrative proxy (-6.56, 107.44)
5. **Karawang**: Administrative proxy (-6.30, 107.30)
6. **Sukabumi**: Administrative proxy (-6.92, 106.93)
7. **Cirebon**: Administrative proxy (-6.73, 108.56)

## Verification Status
- CDS API Client configured locally and verified against `https://cds.climate.copernicus.eu/api`.
- Parameter schema verified directly from ECMWF OpenAPI catalogue:
  - Latitude/Longitude bounding box requires grid-covering extent (0.1° AgERA5 native resolution).
  - Date format requires ISO-8601 interval `yyyy-mm-dd/yyyy-mm-dd`.
  - Format: CSV.
- Pilot execution validated: 4 variables pilot and full 24-variable pilot executed successfully on ECMWF CDS infrastructure.

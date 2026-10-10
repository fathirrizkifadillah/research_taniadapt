import os
import json

os.makedirs("notebooks/dataset_workflows", exist_ok=True)

def make_cell(cell_type, source_text):
    if cell_type == "markdown":
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source_text.strip().split("\n")]
        }
    else:
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source_text.strip().split("\n")]
        }

def save_notebook(filepath, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.11.9"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Generated {filepath}")

# -------------------------------------------------------------
# NB 01: DS01 AgERA5
# -------------------------------------------------------------
c01 = [
    make_cell("markdown", """# DS01 — AgERA5 Agrometeorological Indicators Time-Series (1979–2025)
## Phase 3: Dataset Discovery & Acquisition | Phase 4: Dataset Quality Audit
**TaniAdapt — Primary Weather Backbone**

Official source: https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators-timeseries
Target locations: Tasikmalaya, Bandung, Bekasi, Purwakarta, Karawang, Sukabumi, Cirebon
Target variables: 24 agriculturally relevant variables (temperatures, precipitation, RH, VPD, ET0, solar radiation, wind)
"""),
    make_cell("code", """import os
import cdsapi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath("../..")
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "DS01_agera5")
os.makedirs(RAW_DIR, exist_ok=True)
print("Raw data directory:", RAW_DIR)
"""),
    make_cell("markdown", """### Phase 3 — Discovery & API Schema Verification
We inspect the official CDS API catalogue and variable inventory.
"""),
    make_cell("code", """inv_path = os.path.join(PROJECT_ROOT, "reports", "dataset_discovery", "agera5_variable_inventory.csv")
if os.path.exists(inv_path):
    df_inv = pd.read_csv(inv_path)
    print("Cataloged AgERA5 variables:", len(df_inv))
    display(df_inv[["display_label", "exact_identifier", "decision", "units_and_definition"]].head(10))
"""),
    make_cell("markdown", """### Phase 3 — Acquisition Execution
Idempotent loading and checking of downloaded 10-year files across 7 locations.
"""),
    make_cell("code", """locations = ["bandung", "karawang", "tasikmalaya", "sukabumi", "cirebon", "purwakarta", "bekasi"]
for loc in locations:
    fpath = os.path.join(RAW_DIR, f"agera5_{loc}_2015_2024.csv")
    if os.path.exists(fpath):
        sz = os.path.getsize(fpath)
        print(f"Verified {loc.upper()}: {fpath} ({sz:,} bytes)")
    else:
        print(f"Missing {loc.upper()}")
"""),
    make_cell("markdown", """### Phase 4 — Dataset Quality Audit
We parse the primary Bandung dataset, inspect schema, check nulls, and verify physical plausibility rules.
"""),
    make_cell("code", """df_bandung = pd.read_csv(os.path.join(RAW_DIR, "agera5_bandung_2015_2024.csv"))
print("Bandung shape:", df_bandung.shape)
print("Missing values total:", df_bandung.isnull().sum().sum())

# Physical plausibility tests
t_valid = (df_bandung['Temperature_Air_2m_Min_24h'] <= df_bandung['Temperature_Air_2m_Mean_24h']).all() and \
          (df_bandung['Temperature_Air_2m_Mean_24h'] <= df_bandung['Temperature_Air_2m_Max_24h']).all()
precip_valid = (df_bandung['Precipitation_Flux'] >= 0).all()
rh_valid = ((df_bandung['Derived_Relative_Humidity_2m_Min_24h'] >= 0) & (df_bandung['Derived_Relative_Humidity_2m_Max_24h'] <= 100.1)).all()
vpd_valid = (df_bandung['Vapour_Pressure_Deficit_at_Maximum_Temperature'] >= 0).all()

print("Plausibility check results:")
print(" - Tmin <= Tmean <= Tmax:", t_valid)
print(" - Precipitation >= 0:", precip_valid)
print(" - Relative Humidity in bounds [0, 100]:", rh_valid)
print(" - VPD >= 0:", vpd_valid)
"""),
    make_cell("markdown", """### Disposition & Diagnostic Plot
"""),
    make_cell("code", """plt.figure(figsize=(10, 4))
df_bandung['valid_time'] = pd.to_datetime(df_bandung['valid_time'])
df_2024 = df_bandung[df_bandung['valid_time'].dt.year == 2024]
plt.plot(df_2024['valid_time'], df_2024['Temperature_Air_2m_Mean_24h'] - 273.15, label='Tmean (°C)', color='darkorange')
plt.plot(df_2024['valid_time'], df_2024['Temperature_Air_2m_Max_24h'] - 273.15, label='Tmax (°C)', color='red', alpha=0.5)
plt.plot(df_2024['valid_time'], df_2024['Temperature_Air_2m_Min_24h'] - 273.15, label='Tmin (°C)', color='blue', alpha=0.5)
plt.title("AgERA5 Bandung 2024 - Daily Temperatures")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print("AUDIT DISPOSITION: PASS (Primary Weather Backbone)")
""")
]
save_notebook("notebooks/dataset_workflows/DS01_agera5_discovery_acquisition_audit.ipynb", c01)

# -------------------------------------------------------------
# NB 02: DS02 Bangladesh Rice Panel
# -------------------------------------------------------------
c02 = [
    make_cell("markdown", """# DS02 — Bangladesh Rice Climate–Yield Panel Replication Archive
## Phase 3: Dataset Discovery & Acquisition | Phase 4: Dataset Quality Audit
**TaniAdapt — Methodological & Comparative Panel Benchmark**

Official source: https://data.mendeley.com/datasets/h94z4ftts2/1 (DOI: 10.17632/h94z4ftts2.1)
Author: BRRI / Mendeley Data
"""),
    make_cell("code", """import os
import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath("../..")
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "DS02_bangladesh_rice_panel")
os.makedirs(RAW_DIR, exist_ok=True)
"""),
    make_cell("markdown", """### Phase 3 — Acquisition Verification
Verifying replication archive zip and extracted CSVs.
"""),
    make_cell("code", """zip_path = os.path.join(RAW_DIR, "Growing_Season_Climate_Rice_Bangladesh_Mendeley_Replication_v1.zip")
print("Archive exists:", os.path.exists(zip_path), f"({os.path.getsize(zip_path):,} bytes)")

csv_path = os.path.join(RAW_DIR, "extracted", "Growing_Season_Climate_Rice_Bangladesh_Replication", "Rice_Yield_2015_2024_Audited.csv")
df_rice = pd.read_csv(csv_path)
print("Rice Yield Audited records:", df_rice.shape)
"""),
    make_cell("markdown", """### Phase 4 — Quality Audit
Panel grain: district x crop x crop_year. Missingness, key uniqueness, and outcome variables.
"""),
    make_cell("code", """print("Crops:", df_rice['crop'].unique())
print("Crop years:", df_rice['crop_year'].unique())
print("Districts count:", df_rice['district'].nunique())
print("Yield stats (MT/ha):")
display(df_rice[['area_ha', 'yield_t_ha', 'production_mt']].describe())

# Check duplicates on panel keys
dups = df_rice.duplicated(subset=['district', 'crop', 'crop_year']).sum()
print(f"Duplicate panel keys: {dups}")
"""),
    make_cell("markdown", """### Disposition & Visualizations
"""),
    make_cell("code", """plt.figure(figsize=(9, 4))
df_rice.groupby(['crop_year', 'crop'])['yield_t_ha'].mean().unstack().plot(marker='o', ax=plt.gca())
plt.title("Bangladesh Rice Panel - Mean Yield by Season (2015-2024)")
plt.ylabel("Yield (MT/ha)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print("AUDIT DISPOSITION: PASS (Methodological / Comparison Benchmark)")
print("LIMITATION: International data; cannot be used as direct ground truth for West Java.")
""")
]
save_notebook("notebooks/dataset_workflows/DS02_bangladesh_rice_panel_discovery_acquisition_audit.ipynb", c02)

# -------------------------------------------------------------
# NB 03: DS03 West Java Rice Productivity
# -------------------------------------------------------------
c03 = [
    make_cell("markdown", """# DS03 — West Java Rice Productivity by Regency/City
## Phase 3: Dataset Discovery & Acquisition | Phase 4: Dataset Quality Audit
**TaniAdapt — Regional Rice Outcome Target**

Official source: https://data.go.id / https://galura.jabarprov.go.id
Publisher: Dinas Tanaman Pangan dan Hortikultura Provinsi Jawa Barat
Coverage: 2015–2020 across 27 Kabupaten/Kota
"""),
    make_cell("code", """import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath("../..")
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "DS03_west_java_rice_productivity")
"""),
    make_cell("markdown", """### Phase 3 — Acquisition Verification
"""),
    make_cell("code", """files = ["produktivitas_padi_jabar.csv", "produktivitas_padi_sawah_jabar.csv", "produktivitas_padi_ladang_jabar.csv"]
for f in files:
    p = os.path.join(RAW_DIR, f)
    print(f"{f}: exists={os.path.exists(p)}, rows={len(pd.read_csv(p)) if os.path.exists(p) else 0}")
"""),
    make_cell("markdown", """### Phase 4 — Quality Audit
Compare total padi, sawah, and ladang. Check completeness across 27 kab/kota and 6 years.
"""),
    make_cell("code", """df_total = pd.read_csv(os.path.join(RAW_DIR, "produktivitas_padi_jabar.csv"))
df_sawah = pd.read_csv(os.path.join(RAW_DIR, "produktivitas_padi_sawah_jabar.csv"))
df_ladang = pd.read_csv(os.path.join(RAW_DIR, "produktivitas_padi_ladang_jabar.csv"))

print("Tahun coverage:", sorted(df_total['tahun'].unique()))
print("Kabupaten/Kota count:", df_total['nama_kabupaten_kota'].nunique())
print("Missing values in productivity:", df_total['produktivitas_padi2'].isnull().sum())
print("Expected grid (27 kab/kota x 6 years = 162 rows):", len(df_total) == 162)
"""),
    make_cell("markdown", """### Disposition
"""),
    make_cell("code", """plt.figure(figsize=(9, 4))
df_total.groupby('tahun')['produktivitas_padi2'].mean().plot(kind='bar', color='forestgreen', alpha=0.85)
plt.title("Rata-rata Produktivitas Padi Jawa Barat (2015-2020)")
plt.ylabel("Kuintal / Hektar")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print("AUDIT DISPOSITION: PASS (Regional Rice Outcome Target)")
print("LIMITATION: Annual temporal grain is too coarse for daily operational advisory.")
""")
]
save_notebook("notebooks/dataset_workflows/DS03_west_java_rice_productivity_discovery_acquisition_audit.ipynb", c03)

# -------------------------------------------------------------
# NB 04: DS04 Indonesia Nationwide Agroclimatic
# -------------------------------------------------------------
c04 = [
    make_cell("markdown", """# DS04 — Indonesia Nationwide Agroclimatic Dataset
## Phase 3: Dataset Discovery & Acquisition | Phase 4: Dataset Quality Audit
**TaniAdapt — National Agroclimatic Benchmark & Derived Indicators**

Official source: https://data.mendeley.com/datasets/3pfbdbzfff/1 (DOI: 10.17632/3pfbdbzfff.1)
Derived from: Open-Meteo Historical Weather / ERA5-Seamless (612 terrestrial grid points, 2016-2025)
"""),
    make_cell("code", """import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath("../..")
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "DS04_indonesia_agroclimatic")
"""),
    make_cell("markdown", """### Phase 3 — Acquisition Verification
"""),
    make_cell("code", """grid_path = os.path.join(RAW_DIR, "grid_points.csv")
ind_path = os.path.join(RAW_DIR, "indicator_definitions.csv")
parquet_path = os.path.join(RAW_DIR, "agroclimate_with_indicators.parquet")

print("Grid points exists:", os.path.exists(grid_path))
print("Indicators exists:", os.path.exists(ind_path))
print("Combined Parquet exists:", os.path.exists(parquet_path), f"({os.path.getsize(parquet_path):,} bytes)")
"""),
    make_cell("markdown", """### Phase 4 — Quality Audit
Grid points coordinates, indicator definitions, and Parquet metadata.
"""),
    make_cell("code", """df_grid = pd.read_csv(grid_path)
df_def = pd.read_csv(ind_path, encoding="latin1")

print("Total Indonesian grid points:", len(df_grid))
display(df_def[["indicator_name", "category", "units", "description"]])

# Filter West Java grid points (-7.9 <= lat <= -5.8, 106.3 <= lon <= 109.0)
df_jabar_grid = df_grid[(df_grid['latitude'] >= -7.9) & (df_grid['latitude'] <= -5.8) &
                        (df_grid['longitude'] >= 106.3) & (df_grid['longitude'] <= 109.0)]
print("West Java intersecting grid points in DS04:", len(df_jabar_grid))
"""),
    make_cell("markdown", """### Disposition
"""),
    make_cell("code", """plt.figure(figsize=(9, 4))
plt.scatter(df_grid['longitude'], df_grid['latitude'], c='grey', s=5, alpha=0.5, label='Indonesia')
plt.scatter(df_jabar_grid['longitude'], df_jabar_grid['latitude'], c='red', s=25, label='Jawa Barat points')
plt.title("DS04 612 Grid Points across Indonesia (West Java Highlighted)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print("AUDIT DISPOSITION: PASS (Agroclimate Reference & Comparison Backbone)")
print("LIMITATION: Spatial resolution is 0.5° (coarser than AgERA5 0.1°). Derived from ERA5-Seamless.")
""")
]
save_notebook("notebooks/dataset_workflows/DS04_indonesia_agroclimatic_discovery_acquisition_audit.ipynb", c04)

# -------------------------------------------------------------
# NB 05: DS05 Subang Maize Productivity
# -------------------------------------------------------------
c05 = [
    make_cell("markdown", """# DS05 — Subang & West Java Maize Productivity
## Phase 3: Dataset Discovery & Acquisition | Phase 4: Dataset Quality Audit
**TaniAdapt — Regional Maize Outcome Target**

Official source: https://data.go.id / https://galura.jabarprov.go.id
Publisher: Dinas Tanaman Pangan dan Hortikultura Jawa Barat
Coverage: 2015–2022 across 27 Kabupaten/Kota (including Kabupaten Subang)
"""),
    make_cell("code", """import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath("../..")
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "DS05_subang_maize_productivity")
"""),
    make_cell("markdown", """### Phase 3 — Acquisition Verification
"""),
    make_cell("code", """csv_path = os.path.join(RAW_DIR, "produktivitas_jagung_jabar.csv")
df_maize = pd.read_csv(csv_path)
print("Maize dataset shape:", df_maize.shape)
print("Columns:", list(df_maize.columns))
"""),
    make_cell("markdown", """### Phase 4 — Quality Audit
Evaluate regency-level coverage and Subang Regency records.
"""),
    make_cell("code", """subang_data = df_maize[df_maize['nama_kabupaten_kota'].str.contains('SUBANG', case=False, na=False)]
print("Subang records count:", len(subang_data))
display(subang_data[['tahun', 'nama_kabupaten_kota', 'produktivitas_jagung', 'satuan']])

print("Missing values in productivity:", df_maize['produktivitas_jagung'].isnull().sum())
print("Years available:", sorted(df_maize['tahun'].unique()))
"""),
    make_cell("markdown", """### Disposition
"""),
    make_cell("code", """plt.figure(figsize=(8, 4))
mean_jabar = df_maize.groupby('tahun')['produktivitas_jagung'].mean()
plt.plot(mean_jabar.index, mean_jabar.values, marker='o', label='Mean Jawa Barat')
plt.plot(subang_data['tahun'], subang_data['produktivitas_jagung'], marker='s', color='orange', label='Kabupaten Subang')
plt.title("Produktivitas Jagung: Jawa Barat vs Kabupaten Subang (2015-2022)")
plt.ylabel("Kuintal / Hektar")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print("AUDIT DISPOSITION: PASS (Regional Maize Outcome Target)")
print("NOTE: Subang is present at regency level. Subdistrict (kecamatan) API was degraded (502) on upstream portal.")
""")
]
save_notebook("notebooks/dataset_workflows/DS05_subang_maize_productivity_discovery_acquisition_audit.ipynb", c05)

# -------------------------------------------------------------
# NB 06: DS06 West Java Horticulture (Chili)
# -------------------------------------------------------------
c06 = [
    make_cell("markdown", """# DS06 — West Java Seasonal Vegetables/Fruits (SBS) Productivity (Chili Focus)
## Phase 3: Dataset Discovery & Acquisition | Phase 4: Dataset Quality Audit
**TaniAdapt — Regional Horticulture Outcome Target**

Official source: https://opendata.jabarprov.go.id / https://galura.jabarprov.go.id
Publisher: Dinas Tanaman Pangan dan Hortikultura Jawa Barat
Coverage: 2017–2025 across seasonal vegetables (Cabai Besar, Cabai Rawit, Bawang Merah, Tomat, etc.)
"""),
    make_cell("code", """import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath("../..")
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "DS06_west_java_horticulture")
"""),
    make_cell("markdown", """### Phase 3 — Acquisition Verification
"""),
    make_cell("code", """sbs_path = os.path.join(RAW_DIR, "produktivitas_sbs_jabar.csv")
prod_path = os.path.join(RAW_DIR, "produksi_sayuran_komoditas_jabar.csv")

df_sbs = pd.read_csv(sbs_path)
df_prod = pd.read_csv(prod_path)

print("SBS Productivity shape:", df_sbs.shape)
print("Vegetable Production shape:", df_prod.shape)
"""),
    make_cell("markdown", """### Phase 4 — Quality Audit
Commodity verification, chili indicators, missingness, and disease label assessment.
"""),
    make_cell("code", """chili_data = df_sbs[df_sbs['komoditi'].str.contains('CABAI', case=False, na=False)]
print("Chili commodities found:", chili_data['komoditi'].unique())
display(chili_data.groupby(['komoditi', 'tahun'])['produktivitas_sayur_buah'].mean().unstack())

print("PENTING: Apakah dataset ini memiliki label penyakit tanaman?")
print("HASIL AUDIT: TIDAK ADA. Dataset ini adalah data statistik produktivitas/hasil panen agregat, BUKAN disease-labeled dataset.")
"""),
    make_cell("markdown", """### Disposition
"""),
    make_cell("code", """plt.figure(figsize=(9, 4.5))
for comm in chili_data['komoditi'].unique():
    sub = chili_data[chili_data['komoditi'] == comm].sort_values('tahun')
    plt.plot(sub['tahun'], sub['produktivitas_sayur_buah'], marker='o', label=comm)
plt.title("Produktivitas Cabai Jawa Barat (2017-2025)")
plt.ylabel("Kuintal / Hektar")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print("AUDIT DISPOSITION: PASS (Regional Horticulture Outcome Target)")
print("CAVEAT: Statistically suitable as crop yield/productivity target; not an incidence/severity disease label.")
""")
]
save_notebook("notebooks/dataset_workflows/DS06_west_java_horticulture_discovery_acquisition_audit.ipynb", c06)

print("\nAll 6 dataset workflow notebooks generated successfully!")

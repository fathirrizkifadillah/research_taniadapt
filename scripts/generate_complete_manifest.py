import os
import hashlib
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
DATA_DIR = PROJECT_ROOT / "data"

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def get_actual_columns(filepath):
    if not os.path.exists(filepath):
        return ""
    try:
        if str(filepath).endswith(".csv"):
            df = pd.read_csv(filepath, nrows=2)
            return ";".join(df.columns.tolist())
        elif str(filepath).endswith(".parquet"):
            df = pd.read_parquet(filepath)
            return ";".join(df.columns.tolist())
        elif str(filepath).endswith(".json"):
            import json
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "data" in data and len(data["data"]) > 0:
                return ";".join(list(data["data"][0].keys()))
            elif isinstance(data, list) and len(data) > 0:
                return ";".join(list(data[0].keys()))
    except Exception as e:
        return f"Error: {e}"
    return ""

all_27_kabkota = [
    ("kab_bandung", "Kabupaten Bandung"),
    ("kab_bandung_barat", "Kabupaten Bandung Barat"),
    ("kab_bekasi", "Kabupaten Bekasi"),
    ("kab_bogor", "Kabupaten Bogor"),
    ("kab_ciamis", "Kabupaten Ciamis"),
    ("kab_cianjur", "Kabupaten Cianjur"),
    ("kab_cirebon", "Kabupaten Cirebon"),
    ("kab_garut", "Kabupaten Garut"),
    ("kab_indramayu", "Kabupaten Indramayu"),
    ("kab_karawang", "Kabupaten Karawang"),
    ("kab_kuningan", "Kabupaten Kuningan"),
    ("kab_majalengka", "Kabupaten Majalengka"),
    ("kab_pangandaran", "Kabupaten Pangandaran"),
    ("kab_purwakarta", "Kabupaten Purwakarta"),
    ("kab_subang", "Kabupaten Subang"),
    ("kab_sukabumi", "Kabupaten Sukabumi"),
    ("kab_sumedang", "Kabupaten Sumedang"),
    ("kab_tasikmalaya", "Kabupaten Tasikmalaya"),
    ("kota_bandung", "Kota Bandung"),
    ("kota_banjar", "Kota Banjar"),
    ("kota_bekasi", "Kota Bekasi"),
    ("kota_bogor", "Kota Bogor"),
    ("kota_cimahi", "Kota Cimahi"),
    ("kota_cirebon", "Kota Cirebon"),
    ("kota_depok", "Kota Depok"),
    ("kota_sukabumi", "Kota Sukabumi"),
    ("kota_tasikmalaya", "Kota Tasikmalaya")
]

manifest_entries = []

# DS01: Seluruh 27 Kabupaten/Kota AgERA5
for slug, nama in all_27_kabkota:
    manifest_entries.append({
        "id": f"DS01_{slug}",
        "nama": f"AgERA5 {nama} Weather Timeseries (2015-2024)",
        "url_asli": "https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators-timeseries",
        "doi": "10.24381/f9c1f09d",
        "tanggal_unduh": "2026-10-11",
        "versi": "1.0",
        "lisensi": "Copernicus Open Access (CC-BY 4.0)",
        "file_path": f"data/raw/DS01_agera5/agera5_{slug}_2015_2024.csv"
    })

# DS02 - Bangladesh
manifest_entries.extend([
    {"id": "DS02_rice_panel_audited", "nama": "Bangladesh Rice Outcome Panel Audited (2015-2024)", "url_asli": "https://data.mendeley.com/datasets/h94z4ftts2/1", "doi": "10.17632/h94z4ftts2.1", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "CC BY 4.0", "file_path": "data/raw/DS02_bangladesh_rice_panel/extracted/Growing_Season_Climate_Rice_Bangladesh_Replication/Rice_Yield_2015_2024_Audited.csv"},
    {"id": "DS02_rice_weather_merged", "nama": "Bangladesh Rice Climate Merged Panel (2015-2024)", "url_asli": "https://data.mendeley.com/datasets/h94z4ftts2/1", "doi": "10.17632/h94z4ftts2.1", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "CC BY 4.0", "file_path": "data/raw/DS02_bangladesh_rice_panel/extracted/Growing_Season_Climate_Rice_Bangladesh_Replication/03_merge/Phase5_Final_Merged_Primary_2015_2024.csv"},
])

# DS03 - Padi Jabar
manifest_entries.extend([
    {"id": "DS03_padi_total", "nama": "Produktivitas Padi Total Jawa Barat (2015-2020)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/od_18103_produktivitas_padi_berdasarkan_kabupatenkota", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv"},
    {"id": "DS03_padi_sawah", "nama": "Produktivitas Padi Sawah Jawa Barat (2015-2020)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/od_18099_produktivitas_padi_sawah_berdasarkan_kabupatenkota", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_sawah_jabar.csv"},
    {"id": "DS03_padi_ladang", "nama": "Produktivitas Padi Ladang Jawa Barat (2015-2020)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/od_18102_produktivitas_padi_ladang_berdasarkan_kabupatenkota", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_ladang_jabar.csv"},
    {"id": "DS03_padi_produksi", "nama": "Volume Produksi Padi Jawa Barat (2013-2022)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/produksi-padi-berdasarkan-kabupatenkota-di-jawa-barat", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-11", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS03_west_java_rice_productivity/produksi_padi_jabar.csv"},
])

# DS04 - Indonesia Agroclimate
manifest_entries.extend([
    {"id": "DS04_agroclimate_indicators", "nama": "Indonesia Nationwide Agroclimatic Indicators (Parquet)", "url_asli": "https://data.mendeley.com/datasets/3pfbdbzfff/1", "doi": "10.17632/3pfbdbzfff.1", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "CC BY 4.0", "file_path": "data/raw/DS04_indonesia_agroclimatic/agroclimate_with_indicators.parquet"},
    {"id": "DS04_grid_points", "nama": "Indonesia Terrestrial Grid Points Table", "url_asli": "https://data.mendeley.com/datasets/3pfbdbzfff/1", "doi": "10.17632/3pfbdbzfff.1", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "CC BY 4.0", "file_path": "data/raw/DS04_indonesia_agroclimatic/grid_points.csv"},
])

# DS05 - Jagung
manifest_entries.extend([
    {"id": "DS05_jagung", "nama": "Produktivitas Jagung Jawa Barat (2015-2022)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/od_18104_produktivitas_jagung_berdasarkan_kabupatenkota", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv"},
    {"id": "DS05_jagung_produksi", "nama": "Volume Produksi Jagung Jawa Barat (2015-2022)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/produksi-jagung-berdasarkan-kabupatenkota-di-jawa-barat", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-11", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS05_subang_maize_productivity/produksi_jagung_jabar.csv"},
    {"id": "DS05_jagung_luas_panen", "nama": "Luas Panen Jagung Jawa Barat (2015-2022)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/luas-panen-jagung-berdasarkan-kabupatenkota-di-jawa-barat", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-11", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS05_subang_maize_productivity/luas_panen_jagung_jabar.csv"},
])

# DS06 - Hortikultura SBS & Sayuran
manifest_entries.extend([
    {"id": "DS06_sbs_produktivitas", "nama": "Produktivitas Sayuran Buah Semusim Jabar (2017-2024)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/od_18100_produktivitas_sayuran_buah_semusim_berdasarkan_komoditas", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.csv"},
    {"id": "DS06_produksi_sayuran", "nama": "Volume Produksi Sayuran Komoditas Jabar (2016-2024)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/od_18096_produksi_sayuran_berdasarkan_komoditas", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/DS06_west_java_horticulture/produksi_sayuran_komoditas_jabar.csv"},
])

# DS07 - Kedelai
manifest_entries.extend([
    {"id": "DS_EXT_kedelai", "nama": "Produktivitas Kedelai Jawa Barat (2015-2022)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/od_18105_produktivitas_kedelai_berdasarkan_kabupatenkota", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-10", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/produktivitas_kedelai_jabar.csv"},
    {"id": "DS_EXT_kedelai_produksi", "nama": "Volume Produksi Kedelai Jawa Barat (2015-2022)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/produksi-kedelai-berdasarkan-kabupatenkota-di-jawa-barat", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-11", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/produksi_kedelai_jabar.csv"},
    {"id": "DS_EXT_kedelai_luas_panen", "nama": "Luas Panen Kedelai Jawa Barat (2015-2022)", "url_asli": "https://galura.jabarprov.go.id/api/bigdata/luas-panen-kedelai-berdasarkan-kabupatenkota-di-jawa-barat", "doi": "None (Galura Open Data Jabar)", "tanggal_unduh": "2026-10-11", "versi": "1.0", "lisensi": "Open Data Pemerintah Daerah", "file_path": "data/raw/luas_panen_kedelai_jabar.csv"},
])

# CHIRPS Validasi
manifest_entries.extend([
    {"id": "DS_VAL_chirps_tasikmalaya", "nama": "CHIRPS v2 Daily Precipitation Tasikmalaya (2015-2024)", "url_asli": "https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalDailyP05.html", "doi": "10.1038/sdata.2015.66 (Funk et al., 2015)", "tanggal_unduh": "2026-10-11", "versi": "2.0", "lisensi": "Public Domain / CC0", "file_path": "data/raw/CHIRPS/chirps_tasikmalaya_2015_2024.csv"},
    {"id": "DS_VAL_chirps_subang", "nama": "CHIRPS v2 Daily Precipitation Subang (2015-2024)", "url_asli": "https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalDailyP05.html", "doi": "10.1038/sdata.2015.66", "tanggal_unduh": "2026-10-11", "versi": "2.0", "lisensi": "Public Domain / CC0", "file_path": "data/raw/CHIRPS/chirps_subang_2015_2024.csv"},
    {"id": "DS_VAL_chirps_garut", "nama": "CHIRPS v2 Daily Precipitation Garut (2015-2024)", "url_asli": "https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalDailyP05.html", "doi": "10.1038/sdata.2015.66", "tanggal_unduh": "2026-10-11", "versi": "2.0", "lisensi": "Public Domain / CC0", "file_path": "data/raw/CHIRPS/chirps_garut_2015_2024.csv"},
])

# Kovariat Iklim Makro (ONI & DMI)
manifest_entries.extend([
    {"id": "DS_EXT_oni", "nama": "NOAA Oceanic Niño Index (ONI v5)", "url_asli": "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt", "doi": "None (NOAA CPC Operational)", "tanggal_unduh": "2026-10-11", "versi": "5.0", "lisensi": "Public Domain", "file_path": "data/raw/climate_indices/oni.ascii.txt"},
    {"id": "DS_EXT_dmi", "nama": "NOAA Dipole Mode Index (DMI HadISST1.1)", "url_asli": "https://psl.noaa.gov/data/timeseries/month/data/dmi.had.long.csv", "doi": "None (NOAA PSL)", "tanggal_unduh": "2026-10-11", "versi": "1.1", "lisensi": "Public Domain", "file_path": "data/raw/climate_indices/dmi.had.long.csv"}
])

for entry in manifest_entries:
    p = PROJECT_ROOT / entry["file_path"]
    entry["ukuran_bytes"] = p.stat().st_size if p.exists() else 0
    entry["sha256"] = compute_sha256(p)
    entry["nama_kolom_aktual"] = get_actual_columns(p)

df_manifest = pd.DataFrame(manifest_entries)
out_csv = DATA_DIR / "MANIFEST.csv"
df_manifest.to_csv(out_csv, index=False)
print(f"Berhasil memperbarui MANIFEST.csv lengkap ({len(df_manifest)} entries) di: {out_csv}")

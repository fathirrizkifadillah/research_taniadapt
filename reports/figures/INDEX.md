# Index Visualisasi & Manifest Grafik EDA TaniAdapt (Phase 6)

Dokumen ini memuat indeks lengkap seluruh **51 visualisasi grafis** yang dihasilkan secara mandiri dan komputasional (tanpa hardcode) dari 10 notebook analitis proyek TaniAdapt Jawa Barat. Seluruh grafik diekspor dalam resolusi tinggi 200 DPI dan tercatat pada [`figure_manifest.csv`](file:///c:/CODING/research_taniAdapt/reports/figures/figure_manifest.csv).

---

## Notebook 01 — AgERA5 Reanalysis Weather (DS01)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_pemetaan_27_unit_ke_22_sel_grid_elevasi.png`](file:///c:/CODING/research_taniAdapt/reports/figures/01_AgERA5/fig01_pemetaan_27_unit_ke_22_sel_grid_elevasi.png) | 2015-2024 | 22 | AgERA5 | `PASS (22 Sel Unik)` | 5 pasang wilayah berbagi sel grid (Bogor, Cirebon, Bandung, Ciamis-Kota Tasik, Bandung Barat-Cimahi). |
| **FIG02** | [`fig02_klimatologi_bulanan_hujan_p10_p90.png`](file:///c:/CODING/research_taniAdapt/reports/figures/01_AgERA5/fig02_klimatologi_bulanan_hujan_p10_p90.png) | 2015-2024 | 3240 | AgERA5 | `PASS` | Bebas ambang absolut; rentang P10–P90 menggambarkan batas ekstrim basah-kering. |
| **FIG03** | [`fig03_anomali_musiman_dan_tahunan_enso.png`](file:///c:/CODING/research_taniAdapt/reports/figures/01_AgERA5/fig03_anomali_musiman_dan_tahunan_enso.png) | 2015-2024 | 10 | AgERA5 | `PASS` | Penanda ENSO obyektif berbasis z-score. |
| **FIG04** | [`fig04_korelasi_spasial_anomali_pca_22_sel.png`](file:///c:/CODING/research_taniAdapt/reports/figures/01_AgERA5/fig04_korelasi_spasial_anomali_pca_22_sel.png) | 2015-2024 | 120 | AgERA5 | `PASS` | Tepat 2 komponen menjelaskan 84. |
| **FIG05** | [`fig05_distribusi_variabel_hipotesis_hujan_tmax.png`](file:///c:/CODING/research_taniAdapt/reports/figures/01_AgERA5/fig05_distribusi_variabel_hipotesis_hujan_tmax.png) | 2015-2021 | 126 | AgERA5 | `PASS` | Variabilitas antar-tahun nyata (2019 terpanas & terkering). |
| **FIG06** | [`fig06_sd_residual_variabel_cuaca_setelah_fe.png`](file:///c:/CODING/research_taniAdapt/reports/figures/01_AgERA5/fig06_sd_residual_variabel_cuaca_setelah_fe.png) | 2015-2021 | 126 | AgERA5 | `PASS` | Variasi efektif cuaca menyusut tajam setelah mengontrol FE, menjelaskan secara matematis MDE panel yang lebar. |

---

## Notebook 02 — Bangladesh Rice Panel Literature Transfer Benchmark (DS02)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_struktur_panel_distribusi_yield_musim.png`](file:///c:/CODING/research_taniAdapt/reports/figures/02_bangladesh_rice_panel/fig01_struktur_panel_distribusi_yield_musim.png) | 2015-2023 | 1728 | bangladesh_rice_panel | `PASS (Benchmark Panel)` | Panel seimbang 100% tanpa missing value. |
| **FIG02** | [`fig02_dekomposisi_varians_nested_bangladesh.png`](file:///c:/CODING/research_taniAdapt/reports/figures/02_bangladesh_rice_panel/fig02_dekomposisi_varians_nested_bangladesh.png) | 2015-2023 | 1728 | bangladesh_rice_panel | `PASS` | Variasi spasial distrik menyerap 11. |
| **FIG03** | [`fig03_koefisien_twfe_benchmark_transfer.png`](file:///c:/CODING/research_taniAdapt/reports/figures/02_bangladesh_rice_panel/fig03_koefisien_twfe_benchmark_transfer.png) | 2015-2023 | 1728 | bangladesh_rice_panel | `BENCHMARK TRANSFER` | FIG 02. |

---

## Notebook 03 — West Java Rice Productivity & BPS Reconciliation (DS03)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_rekonsiliasi_ds03_berbobot_luas_vs_bps.png`](file:///c:/CODING/research_taniAdapt/reports/figures/03_west_java_rice/fig01_rekonsiliasi_ds03_berbobot_luas_vs_bps.png) | 2015-2020 | 162 | west_java_rice | `CONDITIONAL` | 2015–2017 baseline cocok 100. |
| **FIG02** | [`fig02_rasio_ds03_bps_keseragaman_artefak_2019.png`](file:///c:/CODING/research_taniAdapt/reports/figures/03_west_java_rice/fig02_rasio_ds03_bps_keseragaman_artefak_2019.png) | 2015-2020 | 162 | west_java_rice | `PASS (Artefak Terisolasi)` | Pada 2019 seluruh 27 kabupaten melonjak seragam (median rasio 1. |
| **FIG03** | [`fig03_heatmap_log_diff_yoy_padi_kab_tahun.png`](file:///c:/CODING/research_taniAdapt/reports/figures/03_west_java_rice/fig03_heatmap_log_diff_yoy_padi_kab_tahun.png) | 2015-2020 | 135 | west_java_rice | `PASS` | Kolom 2019 menunjukkan anomali positif serentak di seluruh wilayah Jawa Barat. |
| **FIG04** | [`fig04_padi_sawah_vs_ladang_artefak_2019.png`](file:///c:/CODING/research_taniAdapt/reports/figures/03_west_java_rice/fig04_padi_sawah_vs_ladang_artefak_2019.png) | 2015-2020 | 162 | west_java_rice | `PASS` | Lonjakan semu 2019 terjadi simultan pada sawah (+23. |
| **FIG05** | [`fig05_variasi_dalam_kab_2015_2017_keputusan_t.png`](file:///c:/CODING/research_taniAdapt/reports/figures/03_west_java_rice/fig05_variasi_dalam_kab_2015_2017_keputusan_t.png) | 2015-2017 | 54 | west_java_rice | `PASS (T=3 Rendah)` | Within-CV rata-rata hanya 2. |
| **FIG06** | [`fig06_funnel_cv_vs_luas_panen_baseline.png`](file:///c:/CODING/research_taniAdapt/reports/figures/03_west_java_rice/fig06_funnel_cv_vs_luas_panen_baseline.png) | 2015-2020 | 27 | west_java_rice | `PASS` | Volatilitas hasil panen menyusut seiring bertambahnya luas panen, pola funnel agronomis yang wajar. |

---

## Notebook 04 — Indonesia Agroclimatic Extreme Indicators & Circularity Check (DS04)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_peta_titik_grid_ds04_jabar.png`](file:///c:/CODING/research_taniAdapt/reports/figures/04_indonesia_agroclimatic/fig01_peta_titik_grid_ds04_jabar.png) | 2016-2025 | 12 | indonesia_agroclimatic | `PASS` | Resolusi kasar 0. |
| **FIG02** | [`fig02_korelasi_anomali_ds04_vs_ds01_sirkular.png`](file:///c:/CODING/research_taniAdapt/reports/figures/04_indonesia_agroclimatic/fig02_korelasi_anomali_ds04_vs_ds01_sirkular.png) | 2016-2024 | 108 | indonesia_agroclimatic | `PASS (Sirkular Internal)` | Korelasi anomali tinggi (r = 0. |
| **FIG04** | [`fig04_distribusi_persentil_cdd_tanpa_ambang.png`](file:///c:/CODING/research_taniAdapt/reports/figures/04_indonesia_agroclimatic/fig04_distribusi_persentil_cdd_tanpa_ambang.png) | 2016-2025 | 43836 | indonesia_agroclimatic | `PASS` | Evaluasi kekeringan bebas ambang absolut (P90 berkisar 12–24 hari berturut-turut). |

---

## Notebook 05 — Maize Productivity, Detrending & 2022 Suspect Flag (DS05)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_matriks_ketersediaan_jagung_valid_nol.png`](file:///c:/CODING/research_taniAdapt/reports/figures/05_subang_maize/fig01_matriks_ketersediaan_jagung_valid_nol.png) | 2015-2022 | 181 | subang_maize | `PASS` | FIG 05. |
| **FIG02** | [`fig02_strip_plot_detektor_nilai_identik_2022.png`](file:///c:/CODING/research_taniAdapt/reports/figures/05_subang_maize/fig02_strip_plot_detektor_nilai_identik_2022.png) | 2015-2022 | 181 | subang_maize | `SUSPECT 2022` | Pada 2022, 13 kabupaten memiliki nilai identik 75. |
| **FIG03** | [`fig03_heatmap_log_diff_yoy_jagung.png`](file:///c:/CODING/research_taniAdapt/reports/figures/05_subang_maize/fig03_heatmap_log_diff_yoy_jagung.png) | 2015-2022 | 154 | subang_maize | `PASS` | Pola normal bervariasi pada 2015–2021; anomali artifisial terlihat pada 2022 akibat konvergensi ke angka tunggal. |
| **FIG04** | [`fig04_kabupaten_vs_kota_distribusi_yield_jagung.png`](file:///c:/CODING/research_taniAdapt/reports/figures/05_subang_maize/fig04_kabupaten_vs_kota_distribusi_yield_jagung.png) | 2015-2021 | 158 | subang_maize | `PASS` | Sentra kabupaten memiliki basis produksi stabil, kota non-sentra memiliki volatilitas basis kecil. |
| **FIG05** | [`fig05_subang_tren_sensitivitas_detrend.png`](file:///c:/CODING/research_taniAdapt/reports/figures/05_subang_maize/fig05_subang_tren_sensitivitas_detrend.png) | 2015-2022 | 8 | subang_maize | `PASS` | Tren kemiringan melompat dari +3. |
| **FIG06** | [`fig06_dekomposisi_varians_nested_jagung.png`](file:///c:/CODING/research_taniAdapt/reports/figures/05_subang_maize/fig06_dekomposisi_varians_nested_jagung.png) | 2015-2021 | 124 | subang_maize | `PASS` | Residu setelah FE adalah 47. |

---

## Notebook 06 — West Java Chili Horticulture & Zero Overlap Audit (DS06)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_seri_provinsi_cabai_cv_dihitung.png`](file:///c:/CODING/research_taniAdapt/reports/figures/06_west_java_horticulture/fig01_seri_provinsi_cabai_cv_dihitung.png) | 2017-2024 | 16 | west_java_horticulture | `PASS (Provinsi Only)` | CV rendah (4. |
| **FIG02** | [`fig02_matriks_ketersediaan_variabel_hortikultura.png`](file:///c:/CODING/research_taniAdapt/reports/figures/06_west_java_horticulture/fig02_matriks_ketersediaan_variabel_hortikultura.png) | 2016-2024 | 4 | west_java_horticulture | `AUDIT KEBIJAKAN` | FIG 06. |
| **FIG03** | [`fig03_bukti_zero_temporal_overlap_kabkota.png`](file:///c:/CODING/research_taniAdapt/reports/figures/06_west_java_horticulture/fig03_bukti_zero_temporal_overlap_kabkota.png) | 2013-2024 | 0 | west_java_horticulture | `BLOCKED (Zero Overlap)` | Tumpang tindih temporal = 0 tahun. |

---

## Notebook 07 — Soybean Productivity & ADM2 geoBoundaries Spatial Relations (DS07)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_matriks_ketersediaan_kedelai_17_sentra.png`](file:///c:/CODING/research_taniAdapt/reports/figures/07_soybean_and_geo/fig01_matriks_ketersediaan_kedelai_17_sentra.png) | 2015-2022 | 156 | soybean_and_geo | `PASS` | FIG 07. |
| **FIG02** | [`fig02_strip_plot_dan_sd_spasial_kedelai_2022_suspect.png`](file:///c:/CODING/research_taniAdapt/reports/figures/07_soybean_and_geo/fig02_strip_plot_dan_sd_spasial_kedelai_2022_suspect.png) | 2015-2022 | 156 | soybean_and_geo | `SUSPECT 2022` | Pada 2022 SD spasial menyusut ke 0. |
| **FIG03** | [`fig03_tren_yield_sentra_utama_kedelai.png`](file:///c:/CODING/research_taniAdapt/reports/figures/07_soybean_and_geo/fig03_tren_yield_sentra_utama_kedelai.png) | 2015-2022 | 32 | soybean_and_geo | `PASS` | Sentra utama memiliki hasil panen stabil 14–16 ku/ha; tahun 2022 mengalami anomali imputasi. |
| **FIG04** | [`fig04_peta_poligon_centroid_sel_agera5.png`](file:///c:/CODING/research_taniAdapt/reports/figures/07_soybean_and_geo/fig04_peta_poligon_centroid_sel_agera5.png) | 2015-2024 | 27 | soybean_and_geo | `PASS` | Pemadanan titik terdekat 0. |
| **FIG05** | [`fig05_elevasi_dan_luas_wilayah_kabupaten.png`](file:///c:/CODING/research_taniAdapt/reports/figures/07_soybean_and_geo/fig05_elevasi_dan_luas_wilayah_kabupaten.png) | 2015-2024 | 27 | soybean_and_geo | `PASS` | Kontras topografi antara pantai utara (<50 m) dan pegunungan priangan (>1. |

---

## Notebook 08 — Harvest Area, Production Volume & Log Decomposition (DS08)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_bobot_baseline_luas_panen_2015_2017.png`](file:///c:/CODING/research_taniAdapt/reports/figures/08_production_and_harvest_area/fig01_bobot_baseline_luas_panen_2015_2017.png) | 2015-2017 | 18 | production_and_harvest_area | `PASS` | Garut mendominasi 46. |
| **FIG02** | [`fig02_dekomposisi_log_produksi_luas_yield.png`](file:///c:/CODING/research_taniAdapt/reports/figures/08_production_and_harvest_area/fig02_dekomposisi_log_produksi_luas_yield.png) | 2015-2022 | 168 | production_and_harvest_area | `PASS` | Identitas exact mengonfirmasi 67. |
| **FIG03** | [`fig03_funnel_cv_yield_vs_luas_baseline_jagung.png`](file:///c:/CODING/research_taniAdapt/reports/figures/08_production_and_harvest_area/fig03_funnel_cv_yield_vs_luas_baseline_jagung.png) | 2015-2022 | 27 | production_and_harvest_area | `PASS` | Volatilitas Subang (+56. |
| **FIG04** | [`fig04_eksploratori_luas_panen_vs_hujan_musiman.png`](file:///c:/CODING/research_taniAdapt/reports/figures/08_production_and_harvest_area/fig04_eksploratori_luas_panen_vs_hujan_musiman.png) | 2015-2022 | 4536 | production_and_harvest_area | `EKSPLORATORI` | DESKRIPTIF EKSPLORATORI TANPA INFERENSI KAUSAL. |

---

## Notebook 09 — Macro Climate Covariates (ONI, DMI) & CHIRPS Satellite Audit (DS09)

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_oni_dmi_fase_enso_iod_2015_2024.png`](file:///c:/CODING/research_taniAdapt/reports/figures/09_climate_covariates_and_chirps/fig01_oni_dmi_fase_enso_iod_2015_2024.png) | 2015-2024 | 120 | climate_covariates_and_chirps | `PASS` | Mengidentifikasi fase iklim makro global tanpa ambang lokal buatan. |
| **FIG02** | [`fig02_matriks_kelengkapan_chirps_erddap.png`](file:///c:/CODING/research_taniAdapt/reports/figures/09_climate_covariates_and_chirps/fig02_matriks_kelengkapan_chirps_erddap.png) | 2015-2024 | 81 | climate_covariates_and_chirps | `PARTIAL / BLOCKED (3 Tahun)` | Tahun 2015, 2017–2019, 2021–2023 berstatus BLOCKED karena server NOAA mengembalikan 0 baris. |
| **FIG03** | [`fig03_korelasi_enso_vs_hujan_musiman_wilayah.png`](file:///c:/CODING/research_taniAdapt/reports/figures/09_climate_covariates_and_chirps/fig03_korelasi_enso_vs_hujan_musiman_wilayah.png) | 2015-2024 | 10 | climate_covariates_and_chirps | `PASS` | Korelasi negatif teramati jelas saat El Niño (2015, 2023), namun n=10 memiliki derajat bebas terbatas. |

---

## Notebook 10 — Cross-Dataset Synthesis, Panel Inference & Analytical MDE

| ID Grafik | Berkas PNG | Periode | N Valid | Sumber Data | Status Kualitas | Intisari Temuan Ilmiah |
|---|---|---|---|---|---|---|
| **FIG01** | [`fig01_scatter_anomali_bulanan_agera5_vs_chirps.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig01_scatter_anomali_bulanan_agera5_vs_chirps.png) | 2016-2024 | 936 | cross_dataset_synthesis | `PASS` | Korelasi anomali tinggi (Pearson r = 0. |
| **FIG02** | [`fig02_bias_bertanda_musim_vs_elevasi.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig02_bias_bertanda_musim_vs_elevasi.png) | 2016-2024 | 27 | cross_dataset_synthesis | `PASS` | Pola bias orografis teramati jelas, elevasi tinggi Priangan memiliki bias positif pada MH akibat pemodelan konvektif awan. |
| **FIG03** | [`fig03_uji_sampling_centroid_vs_area_6_kabupaten.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig03_uji_sampling_centroid_vs_area_6_kabupaten.png) | 2016-2024 | 6 | cross_dataset_synthesis | `PASS` | Agregasi poligon spasial mengevaluasi disparitas bias musiman; sampling poligon area berstatus PENDING verifikasi raster. |
| **FIG04** | [`fig04_agera5_vs_ds04_internal_circularity.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig04_agera5_vs_ds04_internal_circularity.png) | 2016-2024 | 36 | cross_dataset_synthesis | `PASS (Sirkular)` | PEMBANDING INTERNAL SIRKULAR ERA5. |
| **FIG05** | [`fig05_matriks_unit_tahun_valid_panel.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig05_matriks_unit_tahun_valid_panel.png) | 2015-2024 | 302 | cross_dataset_synthesis | `PASS` | Menetapkan sampel analisis resmi secara transparan; Jagung & Kedelai memakai 2015–2021, Padi dibatasi T=3 (2015–2017). |
| **FIG06** | [`fig06_distribusi_fitur_cuaca_terdaftar_kabupaten.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig06_distribusi_fitur_cuaca_terdaftar_kabupaten.png) | 2015-2021 | 124 | cross_dataset_synthesis | `PASS` | Menggambarkan kontras hidrologis antar-kabupaten. |
| **FIG07** | [`fig07_added_variable_plot_corn_webb_ci_mde.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig07_added_variable_plot_corn_webb_ci_mde.png) | 2015-2021 | 124 | cross_dataset_synthesis | `PASS (Webb Bootstrap)` | 95% CI Wild Cluster Bootstrap Webb [-0. |
| **FIG08** | [`fig08_forest_loo_tahun_webb_bootstrap.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig08_forest_loo_tahun_webb_bootstrap.png) | 2015-2021 | 124 | cross_dataset_synthesis | `PASS` | Stabilitas estimasi terverifikasi, tidak ada tahun tunggal yang mendikte arah koefisien. |
| **FIG09** | [`fig09_stabilitas_jendela_dan_lead_placebo_dihitung.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig09_stabilitas_jendela_dan_lead_placebo_dihitung.png) | 2015-2021 | 124 | cross_dataset_synthesis | `PASS (Dihitung dari Kode)` | Lead weather t+1 terhitung nyata (β=+0. |
| **FIG10** | [`fig10_tier_b_ifwc_depresiasi_embun_run_length.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig10_tier_b_ifwc_depresiasi_embun_run_length.png) | 2015-2024 | 98631 | cross_dataset_synthesis | `PASS (Tier B Deskriptif)` | Tier B Hortikultura — murni pemantauan mikroklimat deskriptif tanpa regresi yield panen. |
| **FIG11** | [`fig11_mde_per_panel_final_formula_sigma.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig11_mde_per_panel_final_formula_sigma.png) | 2015-2021 | 296 | cross_dataset_synthesis | `PASS (Analitis)` | MDE dihitung penuh dari rumus analitis; peringatan eksplisit dicantumkan bahwa residual padi sempit karena degrees of freedom sedikit. |
| **FIG12** | [`fig12_dekomposisi_varians_per_komoditas.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig12_dekomposisi_varians_per_komoditas.png) | 2015-2021 | 232 | cross_dataset_synthesis | `PASS` | Komponen residu setelah FE diberi label jujur (cuaca lokal + noise + kesalahan ukur, bukan sinyal cuaca murni). |

---
| **FIG04B** | [`fig15_peta_geospasial_bias_presipitasi_elevasi.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig15_peta_geospasial_bias_presipitasi_elevasi.png) | 2016-2024 | 27 | cross_dataset_synthesis | `PASS` | Peta Sintesis Spasial: Bubble elevasi SRTM vs Signed Bias AgERA5 vs CHIRPS. |
| **FIG13** | [`fig13_hindcast_validation_extreme_events.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig13_hindcast_validation_extreme_events.png) | 2015-2024 | 18 | cross_dataset_synthesis | `PASS` | Validasi Non-Yield Hindcast Peristiwa Ekstrem BMKG (2016 Basah 100%, 2019 Kering 100%, 2023 Kering 88.9%). |
| **FIG14** | [`fig14_crop_water_balance_etc.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig14_crop_water_balance_etc.png) | 2019 | 123 | cross_dataset_synthesis | `PASS` | Neraca Air Tanaman per Fase Fenologi ETc Subang MK 2019 (Defisit Lengas Tanah -343.7 mm). |
| **FIG16** | [`fig16_phase7_full_hypotheses_forest_plot_mde.png`](file:///c:/CODING/research_taniAdapt/reports/figures/10_cross_dataset_synthesis/fig16_phase7_full_hypotheses_forest_plot_mde.png) | 2015-2021 | 11 | cross_dataset_synthesis | `PASS (100% Insufficient)` | Phase 7: Forest Plot Pengujian 11 Hipotesis Panel Ekonometrika & Evaluasi Daya MDE. |

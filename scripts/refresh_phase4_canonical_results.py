"""Refresh auditable DS09 and cross-dataset summary values from local outputs."""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from project_paths import PROJECT_ROOT, DATA_RAW, DATA_PROCESSED, REPORTS_DIR
import sys
sys.path.append(str(PROJECT_ROOT / "scripts"))
from eda_utils import wild_cluster_bootstrap_webb, compute_mde_from_boot_se


def result_path(name):
    return REPORTS_DIR / "results" / name


def robust_models():
    d = pd.read_csv(DATA_PROCESSED / "corn_panel_weather_matched.csv")
    area = pd.read_csv(DATA_RAW / "DS05_subang_maize_productivity" / "luas_panen_jagung_jabar.csv")
    d = d.merge(area[["kode_kabupaten_kota", "tahun", "luas_panen"]], on=["kode_kabupaten_kota", "tahun"], how="left")
    base_area = d[d["tahun"].between(2015, 2017)].groupby("nama_kabupaten_kota")["luas_panen"].mean()
    d["w_base"] = d["nama_kabupaten_kota"].map(base_area).fillna(d["luas_panen"])
    d["w"] = d["w_base"] / d["w_base"].mean()

    def ols_resids(x):
        y = sm.OLS.from_formula("log_y ~ C(nama_kabupaten_kota) + C(tahun)", data=x).fit().resid
        z = sm.OLS.from_formula("precip_feb_apr_z ~ C(nama_kabupaten_kota) + C(tahun)", data=x).fit().resid
        return y, z

    y, x = ols_resids(d)
    w_y = sm.WLS.from_formula("log_y ~ C(nama_kabupaten_kota) + C(tahun)", data=d, weights=d["w"]).fit().resid
    w_x = sm.WLS.from_formula("precip_feb_apr_z ~ C(nama_kabupaten_kota) + C(tahun)", data=d, weights=d["w"]).fit().resid
    beta_wls, lo_wls, hi_wls, se_wls = wild_cluster_bootstrap_webb(w_y, w_x, d["nama_kabupaten_kota"], n_boot=999, seed=42)

    # Huber estimator with Webb weights at the district cluster level, B=999.
    fit = sm.RLM(y, sm.add_constant(x), M=sm.robust.norms.HuberT()).fit()
    beta_h = float(np.asarray(fit.params)[1])
    rng = np.random.default_rng(42)
    values = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(.5), np.sqrt(.5), 1.0, np.sqrt(1.5)])
    clusters = d["nama_kabupaten_kota"].to_numpy()
    unique = np.unique(clusters)
    boot_h = []
    for _ in range(999):
        wm = dict(zip(unique, rng.choice(values, size=len(unique))))
        yb = np.asarray(fit.fittedvalues) + np.asarray(fit.resid) * np.array([wm[c] for c in clusters])
        boot_h.append(float(np.asarray(sm.RLM(yb, sm.add_constant(x), M=sm.robust.norms.HuberT()).fit().params)[1]))
    se_h = float(np.std(boot_h, ddof=1))
    lo_h, hi_h = map(float, np.percentile(boot_h, [2.5, 97.5]))

    # Within-district MAD z-screen, P95 empirical cutoff, then the same Webb bootstrap.
    med = d.groupby("nama_kabupaten_kota")["log_y"].transform("median")
    mad = d.groupby("nama_kabupaten_kota")["log_y"].transform(lambda s: np.median(np.abs(s - s.median())))
    fallback = np.median(np.abs(d["log_y"] - d["log_y"].median()))
    scale = np.where(mad > 0, 1.4826 * mad, 1.4826 * fallback)
    d["robust_z"] = np.abs(d["log_y"] - med) / scale
    cutoff = d["robust_z"].quantile(.95)
    clean = d[d["robust_z"] <= cutoff].copy()
    c_y, c_x = ols_resids(clean)
    beta_c, lo_c, hi_c, se_c = wild_cluster_bootstrap_webb(c_y, c_x, clean["nama_kabupaten_kota"], n_boot=999, seed=42)
    return {
        "h_corn_01_wls_baseline": (beta_wls, lo_wls, hi_wls, se_wls, "WLS fixed-effect residualization; Webb wild-cluster bootstrap, cluster=kabupaten, B=999"),
        "h_corn_01_robust_huber": (beta_h, lo_h, hi_h, se_h, "Huber RLM; Webb wild-cluster residual bootstrap, cluster=kabupaten, B=999"),
        "h_corn_01_clean_mad_z": (beta_c, lo_c, hi_c, se_c, f"Within-kabupaten MAD-z screen at empirical P95={cutoff:.4f}; Webb wild-cluster bootstrap, cluster=kabupaten, B=999; dropped={len(d)-len(clean)}"),
    }


def refresh():
    matched = pd.read_csv(DATA_PROCESSED / "chirps_agera5_validation.csv")
    matched = matched.dropna(subset=["agera5_anom", "chirps_anom"]).copy()
    n_by_year = matched.groupby("year").size().to_dict()
    pooled_r = float(stats.pearsonr(matched["agera5_anom"], matched["chirps_anom"])[0])
    within = {int(y): float(stats.pearsonr(g["agera5_anom"], g["chirps_anom"])[0]) for y, g in matched.groupby("year") if g["agera5_anom"].nunique() > 1 and g["chirps_anom"].nunique() > 1}
    by_unit = matched.groupby("nama_kabupaten_kota").apply(lambda g: stats.pearsonr(g["agera5_anom"], g["chirps_anom"])[0] if g["agera5_anom"].nunique() > 1 and g["chirps_anom"].nunique() > 1 else np.nan)
    n_unit_corr = int(by_unit.notna().sum())

    ds09 = json.loads(result_path("09_climate_covariates_and_chirps.json").read_text())
    ds09.update({
        "n_valid_chirps_unit_months": int(len(matched)),
        "n_chirps_unit_months_by_year": {str(k): int(v) for k, v in n_by_year.items()},
        "n_for_pooled_r": int(len(matched)),
        "n_for_within_year_r": {str(k): int(v) for k, v in n_by_year.items()},
        "n_units_for_per_unit_r": n_unit_corr,
        "chirps_r_pooled": round(pooled_r, 4),
        "chirps_r_within": {str(k): round(v, 4) for k, v in within.items()},
        "chirps_r_per_unit_median": round(float(by_unit.median()), 4),
        "five_key_findings": [
            "ONI and DMI cover 120 months from 2015-2024.",
            "CHIRPS benchmark coverage is 2016, 2020, and 2024 only.",
            f"Matched anomaly rows total N={len(matched)}: " + ", ".join(f"{year} N={count}" for year, count in sorted(n_by_year.items())) + ".",
            f"Pooled anomaly correlation is r={pooled_r:.4f}; median per-unit correlation is {float(by_unit.median()):.4f} across {n_unit_corr} units.",
            "Indramayu has two benchmark years and Depok one benchmark year; no missing unit-months are imputed.",
        ],
    })
    result_path("09_climate_covariates_and_chirps.json").write_text(json.dumps(ds09, indent=2) + "\n")

    a4 = json.loads((REPORTS_DIR / "dataset_audit" / "a10_panel_mde_audit.json").read_text())
    cross = json.loads(result_path("10_cross_dataset_synthesis.json").read_text())
    main = a4["corn_main"]
    rice = a4["rice_t3"]
    cross.update({
        "h_corn_01_beta": round(main["beta_hat"], 4), "h_corn_01_ci_webb": [round(main["ci_low"],4), round(main["ci_high"],4)],
        "h_corn_01_boot_se": round(main["boot_se"],4), "h_corn_01_mde_2_8xse": round(main["mde"],4),
        "rice_t3_boot_se": round(rice["boot_se"],4), "rice_t3_mde_2_8xse": round(rice["mde"],4),
        "chirps_validation_pearson_r_pooled": round(pooled_r,4),
        "chirps_validation_pearson_r_within_2016": round(within.get(2016, np.nan),4),
        "chirps_validation_pearson_r_within_2020": round(within.get(2020, np.nan),4),
        "chirps_validation_pearson_r_within_2024": round(within.get(2024, np.nan),4),
        "chirps_validation_pearson_r_per_unit_median": round(float(by_unit.median()),4),
        "chirps_validation_n_pooled": int(len(matched)), "chirps_validation_n_by_year": {str(k):int(v) for k,v in n_by_year.items()}, "chirps_validation_n_units": n_unit_corr,
    })
    robust = robust_models()
    for prefix, (b, lo, hi, se, method) in robust.items():
        cross[prefix + "_beta"] = round(b, 4)
        cross[prefix + "_ci"] = [round(lo,4), round(hi,4)]
        cross[prefix + "_boot_se"] = round(se,4)
        cross[prefix + "_mde"] = round(compute_mde_from_boot_se(se),4)
        cross[prefix + "_inference_method"] = method
    cross["five_key_findings"] = [
        f"CHIRPS versus AgERA5 anomaly correlation pooled r={pooled_r:.4f}, N={len(matched)}; within-year N is recorded by year.",
        "The prior polygon-sampling calculation was modelled from a fixed reduction factor and is not retained as empirical evidence.",
        f"H_CORN_01 beta={main['beta_hat']:+.4f}, Webb CI [{main['ci_low']:+.4f}, {main['ci_high']:+.4f}], MDE={main['mde']:.4f}; evidence is insufficient for a yield-effect claim.",
        "Robust sensitivity estimates and all MDE values use their recorded bootstrap SE and method fields.",
        f"Rice T=3 MDE={rice['mde']:.4f}; the narrow value does not establish high power.",
    ]
    result_path("10_cross_dataset_synthesis.json").write_text(json.dumps(cross, indent=2) + "\n")


if __name__ == "__main__":
    refresh()

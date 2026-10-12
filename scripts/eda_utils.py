"""
Module: eda_utils.py
Description: Standardized utilities for EDA notebooks (01-10) across TaniAdapt.
Encodes PhD-level statistical methods from .agents/skills/data-scientist:
- Colorblind-friendly plotting styles and figure export (DPI 200, figure manifest)
- Wild Cluster Bootstrap Webb (cluster = kabupaten) for panel regressions
- Minimum Detectable Effect (MDE) analytical calculator from two-way FE residualization
- Centralized JSON result writer (single source of truth for reports/readmes)
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Base paths
PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
RESULTS_DIR = REPORTS_DIR / "results"
MANIFEST_FILE = FIGURES_DIR / "figure_manifest.csv"

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Standardized Color Palette (Colorblind friendly)
PALETTE = {
    "primary": "#1d3557",       # Dark navy
    "secondary": "#457b9d",     # Slate blue
    "accent": "#e63946",        # Crimson
    "kabupaten": "#2a9d8f",     # Teal
    "kota": "#e76f51",          # Burnt orange
    "suspect": "#9e9e9e",       # Grey hatch / suspect flag
    "highlight": "#f4a261",     # Warm yellow-orange
    "background": "#f8f9fa"     # Light clean bg
}

def set_taniadapt_style():
    """Sets publication-grade matplotlib parameters."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 9.5,
        "axes.labelweight": "medium",
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "grid.color": "#e0e0e0",
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "figure.titlesize": 12,
        "figure.titleweight": "bold",
        "figure.dpi": 200
    })

def save_eda_figure(fig, nb_name, fig_id, description, n_valid, period, source, quality_flag, caption, source_cols=""):
    """
    Saves a figure to reports/figures/NN_nama/figXX_desc.png at 200 DPI
    and appends metadata to figure_manifest.csv.
    """
    nb_dir = FIGURES_DIR / nb_name
    nb_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{fig_id}_{description}.png"
    filepath = nb_dir / filename
    
    fig.savefig(filepath, dpi=200, bbox_inches="tight")
    
    # Update manifest
    manifest_row = {
        "file": str(filepath.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "notebook": nb_name,
        "dataset": nb_name.split("_", 1)[1] if "_" in nb_name else nb_name,
        "N_valid": int(n_valid) if isinstance(n_valid, (int, np.integer)) else str(n_valid),
        "periode": str(period),
        "flag_kualitas": str(quality_flag),
        "caption": str(caption).replace("\n", " ").strip(),
        "kolom_data_sumber": str(source_cols)
    }
    
    df_new = pd.DataFrame([manifest_row])
    if MANIFEST_FILE.exists():
        df_old = pd.read_csv(MANIFEST_FILE)
        # Avoid exact duplicate row
        df_old = df_old[df_old["file"] != manifest_row["file"]]
        df_updated = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_updated = df_new
        
    df_updated.to_csv(MANIFEST_FILE, index=False)
    return filepath

def write_results_json(nb_name, results_dict):
    """Writes numerical summary results to reports/results/NN_nama.json."""
    out_file = RESULTS_DIR / f"{nb_name}.json"
    
    def convert(o):
        if isinstance(o, (np.int64, np.int32, np.integer)):
            return int(o)
        if isinstance(o, (np.float64, np.float32, np.floating)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if pd.isna(o):
            return None
        return str(o)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results_dict, f, indent=2, default=convert)
    return out_file

def wild_cluster_bootstrap_webb(y_resid, x_resid, cluster_series, n_boot=999, seed=42):
    """
    Wild cluster bootstrap using Webb (1999/2014) 6-point distribution.
    Specifically designed for small number of clusters (G = 14 to 18 sentra kabupaten).
    Returns:
        beta_hat: OLS point estimate on residualized variables
        ci_lower: 2.5 percentile bootstrap estimate
        ci_upper: 97.5 percentile bootstrap estimate
        boot_se: standard deviation of bootstrap estimates
    """
    np.random.seed(seed)
    # Webb 6-point values: +/- sqrt(1.5), +/- 1, +/- sqrt(0.5)
    webb_values = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
    
    x = np.asarray(x_resid)
    y = np.asarray(y_resid)
    clusters = np.asarray(cluster_series)
    unique_clusters = np.unique(clusters)
    G = len(unique_clusters)
    
    # Base OLS estimate
    x_var = np.sum(x**2)
    if x_var == 0:
        return 0.0, 0.0, 0.0, 0.0
    beta_hat = np.sum(x * y) / x_var
    u_hat = y - beta_hat * x
    
    cluster_indices = [np.where(clusters == c)[0] for c in unique_clusters]
    
    boot_betas = []
    for _ in range(n_boot):
        # Draw Webb weight per cluster
        weights = np.random.choice(webb_values, size=G)
        u_boot = np.empty_like(u_hat)
        for g_idx, idxs in enumerate(cluster_indices):
            u_boot[idxs] = u_hat[idxs] * weights[g_idx]
            
        y_boot = beta_hat * x + u_boot
        b_b = np.sum(x * y_boot) / x_var
        boot_betas.append(b_b)
        
    boot_betas = np.array(boot_betas)
    ci_lower = float(np.percentile(boot_betas, 2.5))
    ci_upper = float(np.percentile(boot_betas, 97.5))
    boot_se = float(np.std(boot_betas))
    
    return float(beta_hat), ci_lower, ci_upper, boot_se

def compute_analytical_mde(sigma_y_resid, sigma_x_resid, n_obs, alpha=0.05, power=0.80, df=None):
    """
    Computes analytical Minimum Detectable Effect (MDE) for panel regression:
    MDE = (t_{alpha/2, df} + t_{1-beta, df}) * SE(beta)
    where SE(beta) = sigma_epsilon / (sigma_{x_tilde} * sqrt(N)).
    """
    if df is None:
        df = n_obs - 2
    if df <= 0:
        return np.nan
        
    t_alpha = stats.t.ppf(1 - alpha / 2, df)
    t_power = stats.t.ppf(power, df)
    se_beta = sigma_y_resid / (sigma_x_resid * np.sqrt(n_obs))
    mde = (t_alpha + t_power) * se_beta
    return float(mde)

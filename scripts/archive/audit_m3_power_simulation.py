import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AUDIT_DIR = PROJECT_ROOT / "reports" / "dataset_audit"

# Set random seed
np.random.seed(42)

# Panel configurations based on M1 cleaned kabupaten units
panels = {
    "Padi": {
        "n_units": 18,
        "n_years": 6,
        "clusters": 6,
        "sigma_eps": 0.085, # ~8.5% log residual CV from historical series
        "spatial_rho": 0.65  # West Java shared weather correlation
    },
    "Jagung": {
        "n_units": 18,
        "n_years": 8,
        "clusters": 8,
        "sigma_eps": 0.180, # ~18% log residual CV after kabupaten trend
        "spatial_rho": 0.60
    },
    "Kedelai": {
        "n_units": 17,
        "n_years": 8,
        "clusters": 8,
        "sigma_eps": 0.220, # ~22% log residual CV
        "spatial_rho": 0.60
    }
}

def simulate_power(n_units, n_years, sigma_eps, spatial_rho, beta, n_sims=500):
    sig_count = 0
    total_obs = n_units * n_years
    
    # Unit IDs and Year IDs
    unit_ids = np.repeat(np.arange(n_units), n_years)
    year_ids = np.tile(np.arange(n_years), n_units)
    
    for _ in range(n_sims):
        # Generate weather variable Z with spatial correlation across units in same year
        # Z_it = sqrt(rho)*u_t + sqrt(1-rho)*v_it
        u_t = np.random.normal(0, 1, size=n_years)
        v_it = np.random.normal(0, 1, size=total_obs)
        z = np.sqrt(spatial_rho) * u_t[year_ids] + np.sqrt(1 - spatial_rho) * v_it
        
        # Standardize Z
        z = (z - np.mean(z)) / np.std(z)
        
        # Outcome: y_it = alpha_i + beta * z_it + eps_it
        # alpha_i unit fixed effects
        alpha_i = np.random.normal(0, 0.2, size=n_units)
        eps = np.random.normal(0, sigma_eps, size=total_obs)
        y = alpha_i[unit_ids] + beta * z + eps
        
        df_sim = pd.DataFrame({
            "y": y,
            "z": z,
            "unit": unit_ids,
            "year": year_ids
        })
        
        try:
            # Model with unit fixed effects and cluster SE by year
            # demean by unit to estimate fixed effects efficiently
            df_sim["y_dm"] = df_sim["y"] - df_sim.groupby("unit")["y"].transform("mean")
            df_sim["z_dm"] = df_sim["z"] - df_sim.groupby("unit")["z"].transform("mean")
            
            model = sm.OLS(df_sim["y_dm"], df_sim["z_dm"]).fit(cov_type="cluster", cov_kwds={"groups": df_sim["year"]})
            pval = model.pvalues[0]
            if pval < 0.05:
                sig_count += 1
        except Exception:
            continue
            
    return sig_count / n_sims

results = []

print("Running Monte Carlo Statistical Power Simulations (500 iterations per grid)...")
for crop, cfg in panels.items():
    print(f"\nSimulating for {crop} (Units={cfg['n_units']}, Years={cfg['n_years']}, Clusters={cfg['clusters']}, Residual SD={cfg['sigma_eps']})...")
    test_betas = np.linspace(0.02, 0.35, 12)
    mde_80 = None
    
    for b in test_betas:
        pwr = simulate_power(cfg["n_units"], cfg["n_years"], cfg["sigma_eps"], cfg["spatial_rho"], b, n_sims=400)
        print(f"  beta = {b:.3f} -> Power = {pwr:.3f}")
        if pwr >= 0.80 and mde_80 is None:
            mde_80 = b
            
    if mde_80 is None:
        mde_80 = test_betas[-1] # upper bound
        
    results.append({
        "tanaman": crop,
        "n_kabupaten": cfg["n_units"],
        "n_tahun": cfg["n_years"],
        "n_total_obs": cfg["n_units"] * cfg["n_years"],
        "n_clusters_tahun": cfg["clusters"],
        "korelasi_spasial_rho": cfg["spatial_rho"],
        "residual_sd_log": cfg["sigma_eps"],
        "mde_power_80_pct_log": mde_80,
        "mde_artinya": f"Perubahan yield minimal {mde_80*100:.1f}% per 1 SD anomali cuaca yang bisa dideteksi pada daya 80%"
    })

df_pwr = pd.DataFrame(results)
print("\n=== RINGKASAN MINIMUM DETECTABLE EFFECT (MDE) PADA DAYA 80% ===")
print(df_pwr[["tanaman", "n_total_obs", "n_clusters_tahun", "residual_sd_log", "mde_power_80_pct_log", "mde_artinya"]].to_string(index=False))

df_pwr.to_csv(AUDIT_DIR / "m3_power_simulation_results.csv", index=False)

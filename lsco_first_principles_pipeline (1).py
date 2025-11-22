# -*- coding: utf-8 -*-
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os

path = "/mnt/data/beta_H_final.csv"
df = pd.read_csv(path, sep=r"\s+", engine="python", comment="#", header=None).dropna(axis=1, how="all")
T = pd.to_numeric(df.iloc[:,0], errors="coerce").to_numpy()
beta_x1e3 = pd.to_numeric(df.iloc[:,1], errors="coerce").to_numpy()
mask = np.isfinite(T) & np.isfinite(beta_x1e3)
T = T[mask]; beta = (beta_x1e3[mask]*1e-3)
order = np.argsort(T); T = T[order]; beta = beta[order]

k_B_eV = 8.617e-5
dLdT = 1.62e-9
beta0 = lambda th: (th/(2.0*k_B_eV))*dLdT
beta0_100K = beta0(100.0)
theta_star = 0.8e-3*2.0*k_B_eV/dLdT
beta0_theta_star = beta0(theta_star)

xi_A, a_A = 15.0, 3.8
EF_eV, tau_ps = 0.3, 0.1
hbar_eVs = 6.582119569e-16
V_ratio = (xi_A/a_A)**3
N_eff = V_ratio * (EF_eV * (tau_ps*1e-12) / hbar_eVs)

signal = float(np.nanmean(beta))
noise  = float(np.nanstd(np.diff(beta))) if len(beta) > 2 else max(1e-12, float(np.nanstd(beta)))
SNR = signal/noise if noise > 0 else 1.0
dTh_Th = 1.0/np.sqrt(max(N_eff,1.0)*max(SNR,1.0))
dS_S = 1.0/np.sqrt(max(N_eff,1.0))
dB_B = np.sqrt(dTh_Th**2 + dS_S**2)

def corr_len(T, y):
    y = np.asarray(y)-np.nanmean(y)
    if len(y)<5: return 1.0
    ac = np.correlate(y,y,mode="full"); ac=ac[len(ac)//2:]
    if ac[0]!=0: ac = ac/ac[0]
    dT = np.nanmedian(np.diff(T)) if len(T)>1 else 1.0
    idx = np.where(ac<1.0/np.e)[0]
    return float(idx[0]*dT) if len(idx)>0 else 2.0

xi_T = corr_len(T, beta)
def amp_fac(T, Tm, xi):
    T = np.asarray(T); x=(Tm-T)/max(xi,1e-9); a=np.ones_like(T)
    m = x<2.0; a[m]=np.exp(2.0-x[m]); return a

amp = amp_fac(T, float(np.nanmax(T)), xi_T)
dB_stat = beta*dB_B; dB_tot = dB_stat*amp

enh = np.where(beta0_theta_star>0, beta/beta0_theta_star, np.nan)

# Figures
plt.figure(); plt.errorbar(T, beta*1e3, yerr=dB_tot*1e3, fmt='o', markersize=4)
plt.axhline(beta0_theta_star*1e3, linestyle='--'); plt.axhline(beta0_100K*1e3, linestyle=':')
plt.xlabel("Temperature [K]"); plt.ylabel("β_H [10$^{-3}$ T$^{-2}$]")
plt.title("β_H(T) with uncertainties | β0(Θ*≈%.1f K)=%.3fe-3; β0(100K)=%.3fe-3"%(theta_star, beta0_theta_star*1e3, beta0_100K*1e3))
plt.savefig("/mnt/data/lsco_betaH_first_principles_fig1_betaH_with_uncertainty.png", dpi=160, bbox_inches="tight")
plt.close()

plt.figure(); plt.plot(T, enh, 'o-', markersize=4); plt.axhline(1.0, linestyle='--')
plt.yscale("log"); plt.xlabel("Temperature [K]"); plt.ylabel("β_H / β0(Θ*)")
plt.title("Superconducting Enhancement (Θ*≈%.1f K)"%theta_star)
plt.savefig("/mnt/data/lsco_betaH_first_principles_fig2_enhancement.png", dpi=160, bbox_inches="tight")
plt.close()

rel_stat = np.where(beta!=0, (dB_stat/np.abs(beta))*100.0, np.nan)
rel_tot  = np.where(beta!=0, (dB_tot /np.abs(beta))*100.0, np.nan)
plt.figure(); plt.plot(T, rel_stat, '-', linewidth=1.5, label="Statistical")
plt.plot(T, rel_tot, '-', linewidth=1.5, label="Total (with boundary)")
plt.xlabel("Temperature [K]"); plt.ylabel("Relative Uncertainty [%]")
plt.title("Theoretical Uncertainty Decomposition"); plt.legend()
plt.savefig("/mnt/data/lsco_betaH_first_principles_fig3_uncertainty_decomposition.png", dpi=160, bbox_inches="tight")
plt.close()

plt.figure(); plt.plot(T, amp, 'o-', markersize=4); plt.axhline(1.0, linestyle='--')
thr = float(np.nanmax(T)-2.0*xi_T); plt.axvline(thr, linestyle='--')
plt.xlabel("Temperature [K]"); plt.ylabel("Amplification factor")
plt.title("Boundary layer (ξ_T≈%.2f K; boundary if T > %.1f K)"%(xi_T, thr))
plt.savefig("/mnt/data/lsco_betaH_first_principles_fig4_boundary_amplification.png", dpi=160, bbox_inches="tight")
plt.close()

# Save summary CSV
pd.DataFrame({
 "metric":[
  "beta0_theory_Theta_100K [T^-2]","beta0_theory_target_0.8e-3 [T^-2]","Theta_star_for_0.8e-3 [K]",
  "mean_beta_H_measured [T^-2]","SNR_estimate [-]","N_eff_estimate [-]",
  "deltaTheta/Theta (quantum limit)","deltaS/S (Shannon)","delta_beta/beta (stat)",
  "xi_T [K]","avg_relative_uncertainty_total [%]","mean_enhancement_betaH_over_beta0(Theta*) [-]"
 ],
 "value":[
  float(beta0_100K), float(beta0_theta_star), float(theta_star), float(np.nanmean(beta)), float(SNR), float(N_eff),
  float(dTh_Th), float(dS_S), float(dB_B), float(xi_T), float(np.nanmean(rel_tot)), float(np.nanmean(enh))
 ]
}).to_csv("/mnt/data/lsco_betaH_first_principles_summary.csv", index=False)
print("Done. Summary and figures written under /mnt/data/.")


import numpy as np, pandas as pd
from datetime import datetime
from extract_theta_from_optical import (
    MATERIALS, generate_dummy_data, compute_memory_function,
    spectral_measure, extract_theta, extract_theta_full_pipeline
)

def temp_grid(Tc):
    arr = np.array([0.5,0.7,0.9,1.1,1.5,2.0])*Tc
    return np.unique(arr.astype(int))

materials = ['LSCO_x015','YBCO','Bi2212','CaCuO2']
records = []
matrix_rows = []

for key in materials:
    mat = MATERIALS[key]
    Ts = temp_grid(mat.Tc)
    res = extract_theta_full_pipeline(key, Ts, use_dummy=True, energy_method='canonical', verbose=False)

    T_demo = int(max(Ts.min(), min(int(1.1*mat.Tc), Ts.max())))
    w, s1, s2 = generate_dummy_data(key, T_demo, omega_max=5.0, n_points=600)
    M1, M2, Mdiag = compute_memory_function(w, s1, s2, mat.omega_p)
    kk_vio = Mdiag.get('kk_violation', float('nan'))
    kk_ok = bool(Mdiag.get('kk_ok', True))

    thetas = []
    for em in ['canonical','memory','corrected']:
        th, _ = extract_theta(w, spectral_measure(w, s1, method='f-sum'), M1, energy_method=em)
        thetas.append(th)
    import numpy as np
    thetas = np.array(thetas, dtype=float)
    sens = float(np.std(thetas)/np.mean(thetas)) if np.isfinite(thetas).all() and np.mean(thetas)!=0 else float('nan')
    sens_ok = bool(sens < 0.10) if np.isfinite(sens) else False

    agree = float(res['Theta_c_diagnostics']['agreement'])
    agree_ok = bool(agree < 0.10)
    class_ok = bool(res['validation']['within_tolerance'])
    overall = bool(kk_ok and sens_ok and agree_ok and class_ok)

    records.append({
        'Material': mat.name,
        'Structure': mat.structure,
        'Tc_K': float(res['Tc']),
        'Theta_c_eV': float(res['Theta_c']),
        'Theta_c_over_Tc': float(res['ratio']),
        'Expected_ratio': float(MATERIALS[key].expected_ratio),
        'RelError': float(res['validation']['relative_error']),
        'KK_violation': kk_vio,
        'KK_pass': kk_ok,
        'Method_agreement': agree,
        'Method_pass': agree_ok,
        'Sensitivity': sens,
        'Sensitivity_pass': sens_ok,
        'Class_pass': class_ok,
        'Validation_status': res['validation']['status'],
        'Overall_PASS': overall
    })

    matrix_rows.append({
        'Material': mat.name,
        'Gate: KK': kk_ok,
        'Gate: Method': agree_ok,
        'Gate: ε-sensitivity': sens_ok,
        'Gate: Class': class_ok,
        'OVERALL': overall
    })

df = pd.DataFrame(records)
mx = pd.DataFrame(matrix_rows)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
df.to_csv(f"theta_batch_summary_{ts}.csv", index=False)
mx.to_csv(f"theta_batch_gates_{ts}.csv", index=False)
print("DONE")

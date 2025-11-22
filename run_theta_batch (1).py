
import numpy as np, pandas as pd
from datetime import datetime
from extract_theta_from_optical_v2 import MATERIALS, extract_theta_full_pipeline_v2

def temp_grid(Tc):
    arr = np.array([0.5,0.7,0.9,1.1,1.5,2.0])*Tc
    return np.unique(arr.astype(int))

materials = ['LSCO_x015','YBCO','Bi2212','CaCuO2']
records, matrix_rows = [], []

for key in materials:
    mat = MATERIALS[key]
    Ts = temp_grid(mat.Tc)
    res = extract_theta_full_pipeline_v2(key, Ts, use_dummy=True, verbose=False,
                                         kk_method='odd_fft_uniform', enforce_projection=True)
    kk_status = res['diagnostics'][0]['KK']['status'] if res['diagnostics'] else 'N/A'
    kk_area = res['diagnostics'][0]['KK']['f_sum']['area'] if res['diagnostics'] else float('nan')
    records.append({
        'Material': mat.name,
        'Structure': mat.structure,
        'Tc_K': float(res['Tc']),
        'Theta_c_eV': float(res['Theta_c']),
        'Theta_c_over_Tc': float(res['ratio']),
        'Class': res['classification'],
        'Confidence': float(res['confidence']),
        'Validation': res['validation']['status'],
        'KK_gate_status_firstT': kk_status,
        'KK_fsum_area_firstT': kk_area
    })
    matrix_rows.append({
        'Material': mat.name,
        'KK_gate_PASS': kk_status == 'PASS',
        'Validation_PASS': res['validation']['status']=='PASS',
        'OVERALL': (kk_status=='PASS') and (res['validation']['status']=='PASS')
    })

df = pd.DataFrame(records)
mx = pd.DataFrame(matrix_rows)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
df.to_csv(f"theta_batch_summary_v2_{ts}.csv", index=False)
mx.to_csv(f"theta_batch_gates_v2_{ts}.csv", index=False)
print("DONE (v2, causality-first)")

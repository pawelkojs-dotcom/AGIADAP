"""
Statistics - Statistical Analysis Tools
"""
import numpy as np
from scipy import stats

def compute_mean_std(data):
    return np.mean(data), np.std(data)

def t_test(group1, group2):
    t_stat, p_value = stats.ttest_ind(group1, group2)
    return {'t': t_stat, 'p': p_value, 'significant': p_value < 0.05}

def cohen_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

def correlation(x, y):
    return np.corrcoef(x, y)[0,1]

def regression_analysis(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value
    }

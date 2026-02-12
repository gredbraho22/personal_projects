import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, leaves_list

def get_cluster_weights(cov: pd.DataFrame) -> np.ndarray:
    corr = cov.corr()
    dist = ((1 - corr) / 2.)**0.5
    link = linkage(dist, 'single')
    sort_ix = leaves_list(link)
    return sort_ix

def hrp_weights(returns: pd.DataFrame) -> pd.Series:
    """Hierarchical Risk Parity"""
    cov = returns.cov() * 252
    corr = returns.corr()
    sort_ix = get_cluster_weights(cov)

    weights = pd.Series(1, index=returns.columns)
    clusters = [[i] for i in sort_ix]

    while len(clusters) > 1:
        c1, c2 = clusters.pop(0), clusters.pop(0)
        c12 = c1 + c2
        c1_var = get_cluster_var(cov, c1)
        c2_var = get_cluster_var(cov, c2)
        alpha = 1 - c1_var / (c1_var + c2_var)
        weights[c1] *= alpha
        weights[c2] *= 1 - alpha
        clusters.append(c12)

    return weights / weights.sum()

def get_cluster_var(cov: pd.DataFrame, cluster_items: list) -> float:
    cov_slice = cov.loc[cluster_items, cluster_items]
    ivp = 1 / np.diag(cov_slice)
    ivp /= ivp.sum()
    return (ivp @ cov_slice @ ivp)

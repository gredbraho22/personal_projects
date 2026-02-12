import numpy as np
import pandas as pd
from scipy.optimize import minimize

def risk_parity_weights(cov: pd.DataFrame) -> np.ndarray:
    """Classic risk parity – equal risk contribution"""
    n = len(cov)
    def objective(w):
        port_vol = np.sqrt(w @ cov @ w)
        risk_contrib = w * (cov @ w) / port_vol
        return np.sum((risk_contrib - port_vol / n)**2)

    cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = [(0, 1) for _ in range(n)]
    res = minimize(objective, np.ones(n)/n, constraints=cons, bounds=bounds, method='SLSQP')
    return res.x

from pypfopt import HRPOpt, EfficientCVaR
from typing import Dict
import pandas as pd


def hierarchical_risk_parity(returns: pd.DataFrame) -> Dict[str, float]:
    """HRP - often outperforms mean-variance in practice"""
    hrp = HRPOpt(returns)
    hrp.optimize()
    return hrp.clean_weights()


def min_cvar_portfolio(returns: pd.DataFrame, beta: float = 0.9) -> Dict[str, float]:
    ec = EfficientCVaR(expected_returns.mean_historical_return(returns), returns, beta=beta)
    ec.min_cvar()
    return ec.clean_weights()

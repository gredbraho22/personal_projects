from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier
import pandas as pd
from typing import Dict


def optimize_max_sharpe(
    returns: pd.DataFrame,
    risk_free_rate: float = 0.03,
    frequency: int = 252
) -> Dict[str, float]:
    """
    Computes max-Sharpe portfolio weights using historical returns.
    Returns dict of {ticker: weight}
    """
    if returns.empty or len(returns) < 30:
        raise ValueError("Insufficient return data for optimization")

    mu = expected_returns.mean_historical_return(
        returns,
        frequency=frequency
    )
    S = risk_models.sample_cov(
        returns,
        frequency=frequency
    )

    ef = EfficientFrontier(mu, S, risk_free_rate=risk_free_rate)
    ef.max_sharpe()
    weights = ef.clean_weights()

    return weights


def print_portfolio_summary(weights: Dict[str, float], returns: pd.DataFrame):
    """Quick console summary"""
    print("Optimized Portfolio Weights:")
    for asset, w in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        if w > 0.001:
            print(f"  {asset:6}: {w:>6.2%}")

    # Quick performance estimate
    port_returns = returns.dot(pd.Series(weights))
    ann_ret = port_returns.mean() * 252
    ann_vol = port_returns.std() * (252 ** 0.5)
    sharpe = (ann_ret - 0.03) / ann_vol if ann_vol > 0 else 0
    print(f"  Expected ann. return: {ann_ret:.2%}")
    print(f"  Expected ann. vol:    {ann_vol:.2%}")
    print(f"  Sharpe ratio:         {sharpe:.2f}")

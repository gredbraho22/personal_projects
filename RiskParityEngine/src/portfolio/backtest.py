import pandas as pd
import numpy as np
from src.config import config

def run_backtest(returns: pd.DataFrame, weights_df: pd.DataFrame) -> dict:
    """Vectorized backtest with costs & vol targeting"""
    # Align indices
    common_idx = returns.index.intersection(weights_df.index)
    returns = returns.loc[common_idx]
    weights_df = weights_df.loc[common_idx]

    port_returns = (weights_df.shift(1) * returns).sum(axis=1)  # lag weights

    # Transaction costs
    turnover = weights_df.diff().abs().sum(axis=1) / 2
    tcost = turnover * (config.backtest["transaction_cost_bps"] / 10000)
    port_returns -= tcost

    # Volatility targeting & leverage
    rolling_vol = port_returns.rolling(63).std() * np.sqrt(252)
    leverage = config.backtest["target_vol"] / rolling_vol
    leverage = leverage.clip(0.5, config.backtest["max_leverage"])
    port_returns *= leverage

    equity = (1 + port_returns).cumprod() * config.backtest["initial_capital"]

    metrics = {
        "total_return": equity.iloc[-1] / equity.iloc[0] - 1,
        "cagr": (equity.iloc[-1] / equity.iloc[0]) ** (252 / len(equity)) - 1,
        "annual_vol": port_returns.std() * np.sqrt(252),
        "sharpe": port_returns.mean() / port_returns.std() * np.sqrt(252),
        "max_drawdown": (equity / equity.cummax() - 1).min(),
        "calmar": port_returns.mean() * 252 / abs((equity / equity.cummax() - 1).min())
    }

    return {"equity": equity, "returns": port_returns, "metrics": metrics}

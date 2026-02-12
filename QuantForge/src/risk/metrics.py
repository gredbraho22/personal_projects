import pandas as pd
import numpy as np
from scipy.stats import norm


def calculate_var(returns: pd.Series, confidence: float = 0.95, method: str = 'historical') -> float:
    """Value at Risk (parametric or historical)"""
    if method == 'historical':
        sorted_returns = returns.sort_values()
        index = int((1 - confidence) * len(sorted_returns))
        return -sorted_returns.iloc[index]
    elif method == 'parametric':
        mu = returns.mean()
        sigma = returns.std()
        return -(mu + norm.ppf(1 - confidence) * sigma)
    raise ValueError("Method must be 'historical' or 'parametric'")


def calculate_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
    """Conditional Value at Risk (Expected Shortfall) - historical"""
    var = calculate_var(returns, confidence, 'historical')
    tail_returns = returns[returns <= -var]
    return -tail_returns.mean() if not tail_returns.empty else np.nan


def max_drawdown(equity: pd.Series) -> float:
    roll_max = equity.cummax()
    drawdown = equity / roll_max - 1
    return drawdown.min()


def rolling_sharpe(returns: pd.Series, window: int = 252, rf: float = 0.03) -> pd.Series:
    excess = returns - rf / 252
    return excess.rolling(window).mean() / excess.rolling(window).std() * np.sqrt(252)

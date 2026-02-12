import pandas as pd
import numpy as np

def ulcer_index(returns: pd.Series) -> float:
    drawdown = (returns.cumsum() - returns.cumsum().cummax())
    return np.sqrt((drawdown**2).mean()) * np.sqrt(252)

def rolling_sharpe(returns: pd.Series, window: int = 252) -> pd.Series:
    return returns.rolling(window).mean() / returns.rolling(window).std() * np.sqrt(252)

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from src.config import config


class VectorizedBacktester:
    """
    Simple vectorized backtester for multi-asset strategies.
    Supports signal DataFrame where values are -1 (short), 0 (neutral), 1 (long).
    """
    def __init__(
        self,
        prices: pd.DataFrame,
        signals: pd.DataFrame,
        initial_capital: float = None,
        commission: float = None
    ):
        self.prices = prices
        self.signals = signals.reindex(prices.index).ffill().fillna(0)
        self.initial_capital = initial_capital or config.initial_capital
        self.commission = commission or config.commission_bps  # decimal, e.g. 0.0005

        # Align indices
        common_idx = self.prices.index.intersection(self.signals.index)
        self.prices = self.prices.loc[common_idx]
        self.signals = self.signals.loc[common_idx]

    def run(self) -> Dict:
        # Daily returns
        asset_returns = self.prices.pct_change().fillna(0)

        # Position-weighted returns (assuming equal capital allocation per asset when signal != 0)
        position_weights = self.signals.div(self.signals.abs().sum(axis=1), axis=0).fillna(0)
        strategy_returns = (position_weights * asset_returns).sum(axis=1)

        # Apply approximate transaction costs (on signal changes)
        trades = self.signals.diff().abs().sum(axis=1) / 2  # round-trip count
        cost = trades * self.commission
        strategy_returns -= cost

        # Cumulative performance
        equity = self.initial_capital * (1 + strategy_returns).cumprod()
        equity.iloc[0] = self.initial_capital  # ensure start at initial

        # Key metrics
        ann_return = strategy_returns.mean() * 252
        ann_vol = strategy_returns.std() * np.sqrt(252)
        sharpe = ann_return / ann_vol if ann_vol != 0 else 0

        cum_ret = equity.iloc[-1] / equity.iloc[0] - 1
        max_dd = (equity / equity.cummax() - 1).min()

        metrics = {
            "total_return": cum_ret,
            "annualized_return": ann_return,
            "annualized_vol": ann_vol,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_dd,
            "n_days": len(strategy_returns),
        }

        return {
            "equity_curve": equity,
            "daily_returns": strategy_returns,
            "metrics": metrics,
        }


def simple_momentum_signals(prices: pd.DataFrame, window: int = 50) -> pd.DataFrame:
    """Very basic example signal: long if close > SMA(window), else neutral"""
    sma = prices.rolling(window).mean()
    signals = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    signals[prices > sma] = 1.0
    return signals

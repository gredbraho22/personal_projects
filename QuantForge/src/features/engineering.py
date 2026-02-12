import pandas as pd
import pandas_ta as ta
from typing import Optional


def engineer_features(
    prices: pd.DataFrame,
    include_sentiment: bool = False,
    sentiment_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Adds common technical indicators and optional sentiment features.
    Returns a wide DataFrame with multi-index columns: (ticker, feature)
    """
    features_list = []

    for ticker in prices.columns:
        df = pd.DataFrame(index=prices.index)
        df['close'] = prices[ticker]
        df['returns'] = df['close'].pct_change()

        # Momentum / trend
        df['rsi_14'] = ta.rsi(df['close'], length=14)
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        df['macd'] = macd['MACD_12_26_9']
        df['macd_signal'] = macd['MACDs_12_26_9']
        df['macd_hist'] = macd['MACDh_12_26_9']

        # Volatility
        df['atr_14'] = ta.atr(high=df['close'], low=df['close'], close=df['close'], length=14)
        bb = ta.bbands(df['close'], length=20, std=2)
        df['bb_upper'] = bb['BBU_20_2.0']
        df['bb_lower'] = bb['BBL_20_2.0']
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['close']

        # Volume proxy (since yfinance adj close doesn't have volume reliably here)
        df['vol_20'] = df['returns'].rolling(20).std()

        # Lagged returns
        for lag in [1, 3, 5]:
            df[f'returns_lag_{lag}'] = df['returns'].shift(lag)

        features_list.append(df.add_prefix(f"{ticker}_"))

    features = pd.concat(features_list, axis=1)

    if include_sentiment and sentiment_df is not None:
        # Merge daily sentiment (reindex to match prices)
        for ticker in prices.columns:
            sent_col = f"{ticker}_sentiment"
            if sent_col in sentiment_df.columns:
                features = features.join(
                    sentiment_df[[sent_col]].reindex(features.index, method='ffill'),
                    how='left'
                )

    # Drop rows with any NaN (conservative)
    features = features.dropna()

    return features

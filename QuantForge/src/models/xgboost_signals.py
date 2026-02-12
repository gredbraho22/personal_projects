import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from xgboost import XGBClassifier
from typing import Tuple, Optional
from src.features.engineering import engineer_features


def prepare_ml_targets(prices: pd.DataFrame, horizon: int = 1) -> pd.Series:
    """
    Binary target: 1 if next 'horizon' days return > 0, else 0.
    Shifted backward so we can predict future from current features.
    """
    future_returns = prices.pct_change(periods=horizon).shift(-horizon)
    target = (future_returns > 0).astype(int)
    return target


def train_xgboost_classifier(
    prices: pd.DataFrame,
    horizon: int = 5,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[XGBClassifier, pd.DataFrame]:
    """
    Trains a simple XGBoost model per asset to predict positive/negative return.
    Returns trained model + feature importance DataFrame.
    """
    features = engineer_features(prices)  # no sentiment for simplicity here
    targets = prepare_ml_targets(prices, horizon=horizon)

    # Align indices
    common_idx = features.index.intersection(targets.index)
    X = features.loc[common_idx]
    y = targets.loc[common_idx]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False, random_state=random_state
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=random_state,
        eval_metric='logloss',
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    probas = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, probas)

    print(f"XGBoost - Accuracy: {acc:.4f} | AUC: {auc:.4f} (test set)")

    # Feature importance
    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    return model, importance


def generate_xgboost_signals(
    prices: pd.DataFrame,
    model: XGBClassifier,
    lookback_features: int = 252 * 2  # ~2 years for prediction context
) -> pd.DataFrame:
    """
    Uses the trained model to generate +1 / -1 / 0 signals on recent data.
    Returns signals aligned to prices.
    """
    recent_prices = prices.tail(lookback_features + 10)  # buffer
    features = engineer_features(recent_prices)

    # Predict on the most recent rows (where features are complete)
    X_pred = features.iloc[-len(prices):]  # align back to full prices index if possible

    if X_pred.empty:
        return pd.DataFrame(0, index=prices.index, columns=prices.columns)

    probas = model.predict_proba(X_pred)[:, 1]  # prob of positive return

    # Simple thresholding: >0.6 long, <0.4 short, else neutral
    signals = pd.DataFrame(0, index=prices.index, columns=prices.columns)
    for col in prices.columns:
        ticker_probas = probas  # simplistic: same model per asset for demo
        signals[col] = np.where(ticker_probas > 0.60, 1,
                                np.where(ticker_probas < 0.40, -1, 0))

    # Shift signals forward (trade on next open)
    signals = signals.shift(1).fillna(0)

    return signals

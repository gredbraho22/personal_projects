import lightgbm as lgb
import pandas as pd
from src.config import config

def prepare_lgb_features(df: pd.DataFrame, target_col: str) -> tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[target_col, config.data["date_col"]])
    y = df[target_col]
    return X, y

def train_lightgbm(X: pd.DataFrame, y: pd.Series) -> lgb.LGBMRegressor:
    params = {
        "objective": "regression",
        "metric": "mae",
        "n_estimators": config.models["lightgbm"]["n_estimators"],
        "learning_rate": config.models["lightgbm"]["learning_rate"],
        "max_depth": config.models["lightgbm"]["max_depth"],
        "num_leaves": config.models["lightgbm"].get("num_leaves", 31),
        "verbosity": -1,
        "random_state": 42
    }
    model = lgb.LGBMRegressor(**params)
    model.fit(X, y)
    return model

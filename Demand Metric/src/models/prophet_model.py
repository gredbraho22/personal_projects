from prophet import Prophet
from src.config import config
import pandas as pd
from typing import Dict

def train_prophet_group(group: pd.DataFrame, target_col: str) -> Prophet:
    prophet_df = group.rename(columns={
        config.data["date_col"]: "ds",
        target_col: "y"
    })[["ds", "y"]]

    m = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        changepoint_prior_scale=config.models["prophet"].get("changepoint_prior_scale", 0.05),
        seasonality_mode=config.models["prophet"].get("seasonality_mode", "multiplicative")
    )
    m.fit(prophet_df)
    return m

def forecast_prophet(model: Prophet, horizon: int) -> pd.DataFrame:
    future = model.make_future_dataframe(periods=horizon)
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

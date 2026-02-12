import yfinance as yf
import pandas as pd
from src.config import config

def get_adjusted_prices() -> pd.DataFrame:
    tickers = config.assets["tickers"]
    start = config.assets["start_date"]
    end = config.assets["end_date"]

    df = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)["Close"]
    df = df.dropna(how="all")
    return df.ffill().dropna(how="all")

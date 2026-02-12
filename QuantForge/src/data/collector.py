import yfinance as yf
import pandas as pd
import finnhub
from datetime import datetime
from typing import List, Optional
from src.config import config


class DataCollector:
    def __init__(self):
        if not config.finnhub_api_key:
            raise ValueError("Finnhub API key not found. Set it in config.yaml or FINNHUB_API_KEY env var.")
        self.client = finnhub.Client(config.finnhub_api_key)

    def get_price_data(
        self,
        tickers: Optional[List[str]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> pd.DataFrame:
        tickers = tickers or config.tickers
        start = start or config.start_date
        end = end or config.end_date

        data = yf.download(
            tickers,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True,
            actions=False
        )

        if len(tickers) == 1:
            prices = data["Close"].to_frame(name=tickers[0])
        else:
            prices = data["Close"]

        prices.index = pd.to_datetime(prices.index)
        return prices.dropna(how="all")

    def get_sentiment_data(
        self,
        ticker: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> pd.DataFrame:
        from_date = from_date or config.start_date
        to_date = to_date or config.end_date

        try:
            news = self.client.company_news(
                ticker,
                _from=from_date,
                to=to_date
            )
        except Exception as e:
            print(f"Finnhub error for {ticker}: {e}")
            return pd.DataFrame()

        if not news:
            return pd.DataFrame()

        df = pd.DataFrame(news)
        if "datetime" not in df.columns:
            return pd.DataFrame()

        df["date"] = pd.to_datetime(df["datetime"], unit="s").dt.date
        df = df.groupby("date")["sentiment"].mean().reset_index()
        df = df.rename(columns={"sentiment": f"{ticker}_sentiment"})
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        return df

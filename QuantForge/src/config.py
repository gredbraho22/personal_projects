import os
import yaml
from pathlib import Path
from typing import Dict, Any, List

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        # Priority: environment variable > config.yaml > defaults
        self.data = {}
        self.finnhub = {}
        self.features = {}
        self.backtest = {}
        self.dashboard = {}

        config_path = Path(__file__).parent.parent / "config.yaml"
        if config_path.exists():
            with open(config_path, "r") as f:
                raw = yaml.safe_load(f) or {}
            self.data = raw.get("data", {})
            self.finnhub = raw.get("finnhub", {})
            self.features = raw.get("features", {})
            self.backtest = raw.get("backtest", {})
            self.dashboard = raw.get("dashboard", {})

        # Override with env vars if present
        if api_key := os.getenv("FINNHUB_API_KEY"):
            self.finnhub["api_key"] = api_key

    @property
    def tickers(self) -> List[str]:
        return self.data.get("tickers", ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"])

    @property
    def start_date(self) -> str:
        return self.data.get("start_date", "2020-01-01")

    @property
    def end_date(self) -> str:
        return self.data.get("end_date", "2026-02-01")

    @property
    def finnhub_api_key(self) -> str:
        return self.finnhub.get("api_key", "")

    @property
    def initial_capital(self) -> float:
        return float(self.backtest.get("initial_capital", 100_000))

    @property
    def commission_bps(self) -> float:
        return float(self.backtest.get("commission_bps", 5)) / 10000  # bps → decimal

    @property
    def default_dashboard_tickers(self) -> List[str]:
        return self.dashboard.get("default_tickers", ["AAPL", "MSFT", "NVDA"])


# Global singleton access
config = Config()

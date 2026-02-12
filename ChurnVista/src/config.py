from pathlib import Path
import yaml

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            path = Path(__file__).parent.parent.parent / "config.yaml"
            with open(path) as f:
                cls._instance._data = yaml.safe_load(f) or {}
        return cls._instance

    def __getattr__(self, name):
        return self._data.get(name, {})

config = Config()

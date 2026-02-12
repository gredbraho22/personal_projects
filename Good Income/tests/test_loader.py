import pytest
from src.data.loader import load_data

def test_data_loading():
    df = load_data()
    assert len(df) > 30000
    assert "income" in df.columns
    assert df["income"].dtype == "int"

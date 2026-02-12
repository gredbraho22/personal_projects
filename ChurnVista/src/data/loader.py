import pandas as pd
from src.config import config

def load_customer_data() -> pd.DataFrame:
    df = pd.read_csv(config.data["customer_path"])
    df = df.replace(" ", pd.NA).dropna()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"])
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(int)
    return df

def load_transaction_data() -> pd.DataFrame:
    return pd.read_csv(config.data["transaction_path"])

def merge_data() -> pd.DataFrame:
    cust = load_customer_data()
    trans = load_transaction_data()
    merged = cust.merge(trans, on="customerID", how="left")
    merged["TotalSpend"] = merged.groupby("customerID")["MonthlyCharges"].transform("sum")
    return merged

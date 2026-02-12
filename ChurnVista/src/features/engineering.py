import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # RFM
    df["Recency"] = 12 - df["tenure"]  # months since last "purchase"
    df["Frequency"] = df.groupby("customerID")["MonthlyCharges"].transform("count")
    df["Monetary"] = df["TotalCharges"]

    # LTV proxy
    df["LTV"] = df["MonthlyCharges"] * config.features["ltv_horizon"]

    # Interaction terms
    df["MonthlyCharges_x_tenure"] = df["MonthlyCharges"] * df["tenure"]
    df["Contract_x_Payment"] = df["Contract"] + "_" + df["PaymentMethod"]

    # Buckets
    df["TenureBucket"] = pd.cut(df["tenure"], bins=[0,12,24,48,72], labels=["0-1y","1-2y","2-4y","4+y"])

    # Encode categoricals
    cat_cols = ["gender","Partner","Dependents","PhoneService","MultipleLines","InternetService",
                "OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport","StreamingTV",
                "StreamingMovies","Contract","PaperlessBilling","PaymentMethod","TenureBucket"]
    for col in cat_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

    # Target
    df["Churn"] = (df["Churn"] == "Yes").astype(int)

    return df

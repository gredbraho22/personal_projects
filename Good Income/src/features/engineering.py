import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Age buckets
    df["age_group"] = pd.cut(df["age"], 
                             bins=config.features["age_bins"], 
                             labels=config.features["age_labels"])
    
    # Capital net
    df["capital_net"] = df["capital_gain"] - df["capital_loss"]
    
    # Interaction terms
    df["education_hours"] = df["education_num"] * df["hours_per_week"]
    df["age_hours"] = df["age"] * df["hours_per_week"]
    
    # High capital flag
    df["high_capital"] = (df["capital_net"] > 5000).astype(int)
    
    # Encode categoricals
    cat_cols = ["workclass", "education", "marital_status", "occupation", 
                "relationship", "race", "sex", "native_country", "age_group"]
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    
    return df

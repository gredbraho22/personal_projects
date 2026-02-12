import pandas as pd
from src.config import config

def load_data() -> pd.DataFrame:
    url = config.data["url"]
    columns = config.data["columns"]
    
    df = pd.read_csv(url, names=columns, header=None, na_values=" ?")
    df = df.dropna()
    
    # Clean target
    df["income"] = df["income"].str.strip().map({">50K": 1, "<=50K": 0})
    
    return df

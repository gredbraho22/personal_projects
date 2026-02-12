import optuna
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import joblib
from src.data.loader import load_data
from src.features.engineering import engineer_features

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 200, 1200),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "reg_alpha": trial.suggest_float("reg_alpha", 0, 10),
        "reg_lambda": trial.suggest_float("reg_lambda", 0, 10),
    }
    
    model = XGBClassifier(**params, random_state=42, eval_metric="auc")
    model.fit(X_train, y_train)
    preds = model.predict_proba(X_val)[:, 1]
    return roc_auc_score(y_val, preds)

def train_model():
    df = load_data()
    df = engineer_features(df)
    
    feature_cols = [c for c in df.columns if c != "income"]
    X = df[feature_cols]
    y = df["income"]
    
    global X_train, X_val, y_train, y_val
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=config.model["test_size"], 
        random_state=config.model["random_state"], stratify=y
    )
    
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=config.model["n_trials"])
    
    best_params = study.best_params
    model = XGBClassifier(**best_params, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, "models/best_xgboost.pkl")
    print(f"Best AUC: {study.best_value:.4f}")
    print("Best params:", best_params)
    return model

# train_hv.py
import os
import sys
import joblib
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("server/logs/train_hv.log"),
        logging.StreamHandler()
    ]
)

# Local import to allow importing from Backend/preprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Backend.preprocess.hv_preprocess import preprocess_hv_input


def evaluate_model(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return rmse, mae, r2


def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    logging.info(f"Model saved to {path}")


def plot_feature_importance(model, feature_names, top_n=15):
    fi = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=fi.values[:top_n], y=fi.index[:top_n])
    plt.title("Top Feature Importances (HV)")
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig("outputs/hv_feature_importance.png")
    logging.info("Saved HV feature importance plot.")


def plot_actual_vs_pred(y_true, y_pred):
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_true, y=y_pred, alpha=0.6)
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    plt.plot(lims, lims, "--r")
    plt.xlabel("Actual (km)")
    plt.ylabel("Predicted (km)")
    plt.title("Actual vs Predicted (HV)")
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig("outputs/hv_actual_vs_predicted.png")
    logging.info("Saved HV actual vs predicted plot.")


def train_hv_model(plot=True):
    logging.info("Starting HV model training pipeline")

    # Load raw data and preprocess it
    raw_hv_df = pd.read_csv("hv.csv")
    # Use preprocess_hv_input for initial batch preprocessing
    hv_df = preprocess_hv_input(raw_hv_df.drop(columns=["range_in_km"]), is_training_data=True)
    
    # Re-attach target variable after initial preprocessing
    hv_df["range_in_km"] = raw_hv_df["range_in_km"].loc[hv_df.index] # Ensure target aligns if rows were dropped

    logging.info(f"Loaded {len(hv_df)} rows after preprocessing.")

    # Features for training are all columns except the target
    X = hv_df.drop(columns=["range_in_km"])
    y = hv_df["range_in_km"]

    logging.info(f"Features for training: {X.columns.tolist()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Hyperparameter grid (example, adjust if needed)
    param_grid = {
        "n_estimators": [100, 200],
        "learning_rate": [0.01, 0.05, 0.1],
        "max_depth": [3, 5, 7],
    }

    # --- REVISED: Corrected typo in objective function ---
    base_model = XGBRegressor(objective="reg:squarederror", random_state=42, n_jobs=-1, enable_categorical=True)
    grid = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        scoring="neg_root_mean_squared_error",
        cv=5,
        verbose=1,
        n_jobs=-1,
    )
    grid.fit(X_train, y_train)

    model = grid.best_estimator_
    logging.info(f"Best hyperparameters: {grid.best_params_}")

    # Refit on all training data
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    # Evaluation
    y_pred = model.predict(X_test)
    rmse, mae, r2 = evaluate_model(y_test, y_pred)
    logging.info("   Tuned Model Metrics (HV):")
    logging.info(f"   RMSE : {rmse:.2f} km")
    logging.info(f"   MAE  : {mae:.2f} km")
    logging.info(f"   R2   : {r2:.4f}")

    # Save model and evaluation artifacts
    os.makedirs("Backend/models", exist_ok=True) # Ensure Backend/models directory exists for saving
    save_model(model, "Backend/models/hv_model.joblib")

    os.makedirs("outputs", exist_ok=True)
    pd.DataFrame({
        "metric": ["RMSE", "MAE", "R2"],
        "value": [rmse, mae, r2]
    }).to_csv("outputs/hv_metrics.csv", index=False)

    # Visualizations
    if plot:
        plot_feature_importance(model, X.columns)
        plot_actual_vs_pred(y_test, y_pred)


if __name__ == "__main__":
    train_hv_model(plot=True)
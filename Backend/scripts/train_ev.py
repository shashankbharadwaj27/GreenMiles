# train_ev.py
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
        logging.FileHandler("server/logs/train_ev.log"),
        logging.StreamHandler()
    ]
)

# Local import to allow importing from Backend/preprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Backend.preprocess.ev_preprocess import preprocess_ev_input


def evaluate_model(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return rmse, mae, r2


def feature_engineering(df):
    """
    Applies feature engineering specific to the EV model training.
    (Note: battery_per_kWh and battery_remaining_kWh are now handled in preprocess_ev_input)
    """
    return df


def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    logging.info(f"Model saved to {path}")


def plot_feature_importance(model, feature_names, top_n=15):
    fi = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=fi.values[:top_n], y=fi.index[:top_n])
    plt.title("Top Feature Importances")
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig("outputs/ev_feature_importance.png")
    logging.info("Saved feature importance plot.")


def plot_actual_vs_pred(y_true, y_pred):
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_true, y=y_pred, alpha=0.6)
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    plt.plot(lims, lims, "--r")
    plt.xlabel("Actual (km)")
    plt.ylabel("Predicted (km)")
    plt.title("Actual vs Predicted")
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    plt.savefig("outputs/ev_actual_vs_predicted.png")
    logging.info("Saved actual vs predicted plot.")


def train_ev_model(plot=True):
    logging.info("Starting EV model training pipeline")

    # Load raw data and preprocess it initially
    raw_ev_df = pd.read_csv("ev_data.csv")
    # Pass the DataFrame to preprocess_ev_input for initial batch processing during training
    ev_df = preprocess_ev_input(raw_ev_df.drop(columns=["electric_range_km"])) # `is_training_data` flag is removed from preprocess_ev_input, so pass just the dataframe
    
    # Re-attach target variable after initial preprocessing
    ev_df["electric_range_km"] = raw_ev_df["electric_range_km"].loc[ev_df.index]

    logging.info(f"Loaded {len(ev_df)} rows after preprocessing.")

    # Apply feature engineering defined in this script (now empty, as derived features moved to preprocess_ev_input)
    ev_df = feature_engineering(ev_df)
    
    # Ensure 'range_per_kWh' is dropped if it somehow got into the DataFrame
    if "range_per_kWh" in ev_df.columns:
        ev_df.drop(columns=["range_per_kWh"], inplace=True)

    # Features for training are all columns except the target
    X = ev_df.drop(columns=["electric_range_km"])
    y = ev_df["electric_range_km"]

    logging.info(f"Features for training: {X.columns.tolist()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Hyperparameter grid
    param_grid = {
        "n_estimators": [100, 200],
        "learning_rate": [0.01, 0.05, 0.1],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
    }

    base_model = XGBRegressor(objective="reg:squarederror", random_state=42, n_jobs=-1, enable_categorical=True) # enable_categorical=True added
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
    logging.info("   Tuned Model Metrics:")
    logging.info(f"   RMSE : {rmse:.2f} km")
    logging.info(f"   MAE  : {mae:.2f} km")
    logging.info(f"   R2   : {r2:.4f}")

    # Save model and evaluation artifacts
    os.makedirs("Backend/models", exist_ok=True)
    save_model(model, "Backend/models/ev_model.joblib")

    os.makedirs("outputs", exist_ok=True)
    pd.DataFrame({
        "metric": ["RMSE", "MAE", "R2"],
        "value": [rmse, mae, r2]
    }).to_csv("outputs/ev_metrics.csv", index=False)

    # Visualizations
    if plot:
        plot_feature_importance(model, X.columns)
        plot_actual_vs_pred(y_test, y_pred)


if __name__ == "__main__":
    train_ev_model(plot=True)
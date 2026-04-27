from __future__ import annotations

import json

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBRegressor
except Exception:  # pragma: no cover
    XGBRegressor = None

from config import DATA_PROCESSED, MODELS_DIR, RANDOM_STATE, TEST_SIZE
from utils import ensure_dirs


def load_model_dataset() -> pd.DataFrame:
    path = DATA_PROCESSED / "cost_of_living_clean.csv"
    if not path.exists():
        raise FileNotFoundError("Run `python src/data_preprocessing.py` first.")
    return pd.read_csv(path)


def prepare_features(df: pd.DataFrame, target: str = "cost_of_living_index"):
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found. Available columns: {list(df.columns)}")

    numeric = df.select_dtypes(include="number").copy()
    if target not in numeric.columns:
        raise ValueError(f"Target column '{target}' must be numeric.")

    X = numeric.drop(columns=[target])
    y = numeric[target]
    return X, y


def evaluate_model(name: str, model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    predictions = model.predict(X_test)
    return {
        "model": name,
        "mae": float(mean_absolute_error(y_test, predictions)),
        "mse": float(mean_squared_error(y_test, predictions)),
        "rmse": float(mean_squared_error(y_test, predictions) ** 0.5),
        "r2": float(r2_score(y_test, predictions)),
    }


def train_models(target: str = "cost_of_living_index") -> pd.DataFrame:
    ensure_dirs([MODELS_DIR])
    df = load_model_dataset()
    X, y = prepare_features(df, target=target)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    models = {
        "linear_regression": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", LinearRegression()),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("model", RandomForestRegressor(n_estimators=300, random_state=RANDOM_STATE)),
            ]
        ),
        "gradient_boosting": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("model", GradientBoostingRegressor(random_state=RANDOM_STATE)),
            ]
        ),
    }

    if XGBRegressor is not None:
        models["xgboost"] = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("model", XGBRegressor(random_state=RANDOM_STATE, objective="reg:squarederror")),
            ]
        )

    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        joblib.dump(model, MODELS_DIR / f"{name}.joblib")
        results.append(evaluate_model(name, model, X_test, y_test))

    results_df = pd.DataFrame(results).sort_values("rmse")
    results_df.to_csv(MODELS_DIR / "model_results.csv", index=False)
    with open(MODELS_DIR / "feature_columns.json", "w", encoding="utf-8") as f:
        json.dump(list(X.columns), f, indent=2)
    return results_df


if __name__ == "__main__":
    print(train_models())

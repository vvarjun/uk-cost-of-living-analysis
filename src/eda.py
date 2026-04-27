from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import DATA_PROCESSED, FIGURES_DIR
from utils import ensure_dirs, save_figure


def load_clean_cost_of_living() -> pd.DataFrame:
    path = DATA_PROCESSED / "cost_of_living_clean.csv"
    if not path.exists():
        raise FileNotFoundError("Run `python src/data_preprocessing.py` first.")
    return pd.read_csv(path)


def plot_top_bottom_cost_of_living(df: pd.DataFrame) -> None:
    country_col = "country"
    index_col = "cost_of_living_index"
    if country_col not in df.columns or index_col not in df.columns:
        print("Skipping top/bottom chart: expected columns not found.")
        return

    top_10 = df.sort_values(index_col, ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_10[country_col], top_10[index_col])
    ax.set_title("Top 10 Countries by Cost of Living Index")
    ax.set_xlabel("Cost of Living Index")
    ax.invert_yaxis()
    save_figure(fig, FIGURES_DIR / "top_10_cost_of_living.png")
    plt.close(fig)

    bottom_10 = df.sort_values(index_col, ascending=True).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(bottom_10[country_col], bottom_10[index_col])
    ax.set_title("Bottom 10 Countries by Cost of Living Index")
    ax.set_xlabel("Cost of Living Index")
    ax.invert_yaxis()
    save_figure(fig, FIGURES_DIR / "bottom_10_cost_of_living.png")
    plt.close(fig)


def plot_cost_component_correlation(df: pd.DataFrame) -> None:
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        print("Skipping correlation heatmap: not enough numeric columns.")
        return

    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Matrix: Cost of Living Indicators")
    save_figure(fig, FIGURES_DIR / "cost_of_living_correlation.png")
    plt.close(fig)


def plot_average_component_breakdown(df: pd.DataFrame) -> None:
    component_cols = [
        "rent_index",
        "groceries_index",
        "restaurant_price_index",
        "local_purchasing_power_index",
    ]
    available = [col for col in component_cols if col in df.columns]
    if not available:
        print("Skipping component breakdown: expected columns not found.")
        return

    averages = df[available].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(averages.index, averages.values)
    ax.set_title("Average Cost-of-Living Component Scores")
    ax.set_ylabel("Average Index Value")
    ax.tick_params(axis="x", rotation=30)
    save_figure(fig, FIGURES_DIR / "average_component_breakdown.png")
    plt.close(fig)


def run_eda() -> None:
    ensure_dirs([FIGURES_DIR])
    df = load_clean_cost_of_living()
    plot_top_bottom_cost_of_living(df)
    plot_cost_component_correlation(df)
    plot_average_component_breakdown(df)
    print(f"EDA figures saved to {FIGURES_DIR}")


if __name__ == "__main__":
    run_eda()

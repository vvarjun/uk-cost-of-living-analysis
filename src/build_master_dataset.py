from __future__ import annotations

import pandas as pd

from config import DATA_PROCESSED
from data_preprocessing import build_processed_datasets


def load_processed_file(filename: str) -> pd.DataFrame:
    path = DATA_PROCESSED / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing processed file: {path}")
    return pd.read_csv(path)


def parse_housing_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(
        series.astype(str).str.strip(),
        format="%b-%y",
        errors="coerce"
    )


def build_housing_cpi_master() -> pd.DataFrame:
    housing = load_processed_file("housing_merged_clean.csv")
    cpi = load_processed_file("cpi_reference_tables_clean.csv")

    print("Housing columns:", housing.columns[:5].tolist())
    print("CPI columns:", cpi.columns[:5].tolist())

    housing["date"] = parse_housing_date(housing["date"])
    cpi["date"] = pd.to_datetime(cpi["date"], errors="coerce")

    housing = housing.dropna(subset=["date"])
    cpi = cpi.dropna(subset=["date"])

    housing["year_month"] = housing["date"].dt.to_period("M").astype(str)
    cpi["year_month"] = cpi["date"].dt.to_period("M").astype(str)

    print("Housing year_month range:", housing["year_month"].min(), housing["year_month"].max())
    print("CPI year_month range:", cpi["year_month"].min(), cpi["year_month"].max())
    print("Common months:", len(set(housing["year_month"]) & set(cpi["year_month"])))

    master = housing.merge(
        cpi.drop(columns=["date"]),
        on="year_month",
        how="inner"
    )

    master = master.sort_values("date")
    return master


def build_summary_dataset() -> pd.DataFrame:
    files = [
        "cost_of_living_clean.csv",
        "gdp_index_clean.csv",
        "food_price_index_clean.csv",
        "producer_price_index_clean.csv",
        "cpi_reference_tables_clean.csv",
        "housing_merged_clean.csv",
    ]

    rows = []

    for file in files:
        df = load_processed_file(file)
        rows.append({
            "dataset": file.replace("_clean.csv", "").replace(".csv", ""),
            "rows": df.shape[0],
            "columns": df.shape[1],
        })

    return pd.DataFrame(rows)


def main() -> None:
    print("Building processed datasets...")
    build_processed_datasets()

    print("\nBuilding master housing + CPI dataset...")
    master = build_housing_cpi_master()

    master_path = DATA_PROCESSED / "master_housing_cpi_dataset.csv"
    master.to_csv(master_path, index=False)

    print(f"Saved: {master_path}")
    print("Master shape:", master.shape)
    print(master.head())

    print("\nBuilding dataset summary...")
    summary = build_summary_dataset()

    summary_path = DATA_PROCESSED / "dataset_summary.csv"
    summary.to_csv(summary_path, index=False)

    print(f"Saved: {summary_path}")
    print(summary)


if __name__ == "__main__":
    main()
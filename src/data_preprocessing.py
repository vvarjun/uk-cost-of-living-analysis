from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from config import DATA_PROCESSED, DATA_RAW, RAW_FILES
from utils import coerce_numeric_columns, ensure_dirs, standardise_columns


def load_dataset(key: str, **kwargs) -> pd.DataFrame:
    """Load a configured CSV or Excel dataset from data/raw."""
    path = DATA_RAW / RAW_FILES[key]

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}. Check data/raw and src/config.py.")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path, encoding="utf-8-sig", **kwargs)

    if suffix in {".xlsx", ".xls"}:
        return load_excel_file(path, **kwargs)

    raise ValueError(f"Unsupported file type: {path.name}")


def load_excel_file(file_path, **kwargs):
 file_path = Path(file_path)

 if "consumer_price_inflation" in file_path.name:
     print("Loading CPI reference table: Table 1")

     df = pd.read_excel(
         file_path,
         sheet_name="Table 1",
         header=None,
         skiprows=14
     )

     df = df.iloc[:, [1, 2, 3, 4, 5, 6, 7]]

     df.columns = [
         "date_raw",
         "cpih_index",
         "cpih_12_month_change",
         "cpi_index",
         "cpi_12_month_change",
         "rpi_index",
         "rpi_12_month_change"
     ]

     df = df.dropna(subset=["date_raw"])

     # Keep only actual CPI rows
     df = df[df["date_raw"].astype(str).str.contains(
         "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec",
         case=False,
         na=False
     )]

     # Extract year when available, then forward-fill it
     df["year"] = df["date_raw"].astype(str).str.extract(r"(\d{4})")
     df["year"] = df["year"].ffill()

     # Extract month
     df["month"] = df["date_raw"].astype(str).str.extract(
         r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
         flags=0
     )

     df["date"] = pd.to_datetime(
         df["month"] + "-" + df["year"],
         format="%b-%Y",
         errors="coerce"
     )

     df = df.dropna(subset=["date"])

     df = df[
         [
             "date",
             "cpih_index",
             "cpih_12_month_change",
             "cpi_index",
             "cpi_12_month_change",
             "rpi_index",
             "rpi_12_month_change",
         ]
     ]

     return df

 return pd.read_excel(file_path, **kwargs)

def clean_generic_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Apply common cleaning steps used across the project."""
    df = standardise_columns(df)
    df = coerce_numeric_columns(df)
    df = df.drop_duplicates()
    return df


def clean_cost_of_living() -> pd.DataFrame:
    df = clean_generic_dataset(load_dataset("cost_of_living"))
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    return df


def clean_uk_wide_index(key: str) -> pd.DataFrame:
    """Clean IMF/World-style wide index files with year columns."""
    df = clean_generic_dataset(load_dataset(key))
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    return df


def _prepare_date_index_file(key: str, suffix: str) -> pd.DataFrame:
    df = clean_generic_dataset(load_dataset(key, header=1))
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "date"})
    df = df.dropna(subset=["date"])
    df = df.add_suffix(suffix).rename(columns={f"date{suffix}": "date"})
    return df


def clean_housing_data() -> pd.DataFrame:
    """Merge UK housing datasets."""
    avg = _prepare_date_index_file("average_house_prices", "_average_price")
    idx = _prepare_date_index_file("housing_price_index", "_index")
    sales = _prepare_date_index_file("property_sales_volume", "_sales_volume")

    merged = avg.merge(idx, on="date", how="inner").merge(sales, on="date", how="inner")

    numeric_cols = merged.select_dtypes(include="number").columns
    merged[numeric_cols] = merged[numeric_cols].fillna(merged[numeric_cols].median())

    return merged


def build_processed_datasets() -> Dict[str, Path]:
    """Clean all raw datasets and save processed CSV versions."""
    ensure_dirs([DATA_PROCESSED])
    outputs: Dict[str, Path] = {}

    # Cost of living
    cost = clean_cost_of_living()
    out = DATA_PROCESSED / "cost_of_living_clean.csv"
    cost.to_csv(out, index=False)
    outputs["cost_of_living"] = out

    # Other datasets
    for key in [
        "spareroom_listings",
        "headline_inflation",
        "gdp_index",
        "food_price_index",
        "producer_price_index",
        "spareroom_gdp_index",
        "spareroom_gdp_index_secondary",
        "cpi_reference_tables",
    ]:
        try:
            df = clean_generic_dataset(load_dataset(key))

            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) > 0:
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

            out = DATA_PROCESSED / f"{key}_clean.csv"
            df.to_csv(out, index=False)

            outputs[key] = out

        except Exception as exc:
            print(f"Skipping {key}: {exc}")

    # Housing merged dataset
    try:
        housing = clean_housing_data()
        out = DATA_PROCESSED / "housing_merged_clean.csv"
        housing.to_csv(out, index=False)
        outputs["housing_merged"] = out
    except Exception as exc:
        print(f"Skipping housing merge: {exc}")

    print("\nProcessed datasets created:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")

    return outputs


if __name__ == "__main__":
    build_processed_datasets()
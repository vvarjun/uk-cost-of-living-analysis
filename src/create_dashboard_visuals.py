from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
FIGURES = PROJECT_ROOT / "outputs" / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)


def save_chart(filename: str) -> None:
    path = FIGURES / filename
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


def load_data():
    housing = pd.read_csv(DATA_PROCESSED / "housing_merged_clean.csv")
    cpi = pd.read_csv(DATA_PROCESSED / "cpi_reference_tables_clean.csv")
    master = pd.read_csv(DATA_PROCESSED / "master_housing_cpi_dataset.csv")

    housing["date"] = pd.to_datetime(
        housing["date"].astype(str).str.strip(),
        format="%b-%y",
        errors="coerce",
    )
    housing = housing.dropna(subset=["date"]).sort_values("date")

    cpi["date"] = pd.to_datetime(cpi["date"], errors="coerce")
    cpi = cpi.dropna(subset=["date"]).sort_values("date")

    master["date"] = pd.to_datetime(master["date"], errors="coerce")
    master = master.dropna(subset=["date"]).sort_values("date")

    return housing, cpi, master


def main() -> None:
    housing, cpi, master = load_data()

    plt.figure(figsize=(10, 5))
    plt.plot(cpi["date"], cpi["cpi_index"])
    plt.title("UK CPI Index Trend")
    plt.xlabel("Date")
    plt.ylabel("CPI Index")
    plt.grid(True)
    save_chart("01_cpi_index_trend.png")

    plt.figure(figsize=(10, 5))
    plt.bar(cpi["date"], cpi["cpi_12_month_change"], width=20)
    plt.title("UK CPI 12-Month Percentage Change")
    plt.xlabel("Date")
    plt.ylabel("12-Month Change (%)")
    plt.grid(True)
    save_chart("02_cpi_12_month_change.png")

    plt.figure(figsize=(10, 5))
    plt.plot(housing["date"], housing["e09000001_average_price"])
    plt.title("City of London Average House Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Average House Price (£)")
    plt.grid(True)
    save_chart("03_city_london_house_price_trend.png")

    plt.figure(figsize=(10, 5))
    plt.plot(housing["date"], housing["e09000001_index"])
    plt.title("City of London House Price Index Trend")
    plt.xlabel("Date")
    plt.ylabel("House Price Index")
    plt.grid(True)
    save_chart("04_city_london_house_price_index.png")

    plt.figure(figsize=(10, 5))
    plt.plot(housing["date"], housing["e09000001_sales_volume"])
    plt.title("City of London Property Sales Volume")
    plt.xlabel("Date")
    plt.ylabel("Sales Volume")
    plt.grid(True)
    save_chart("05_city_london_sales_volume.png")

    norm_cpi = master["cpi_index"] / master["cpi_index"].iloc[0]
    norm_house = (
            master["e09000001_average_price"]
            / master["e09000001_average_price"].iloc[0]
    )

    plt.figure(figsize=(10, 5))
    plt.plot(master["date"], norm_cpi, label="CPI Index (Normalized)")
    plt.plot(master["date"], norm_house, label="House Price (Normalized)")
    plt.title("Housing Prices vs CPI - Normalized Comparison")
    plt.xlabel("Date")
    plt.ylabel("Relative Growth")
    plt.legend()
    plt.grid(True)
    save_chart("06_housing_vs_cpi_normalized.png")

    plt.figure(figsize=(10, 5))
    plt.plot(cpi["date"], cpi["cpi_index"], label="CPI Index")
    plt.plot(cpi["date"], cpi["rpi_index"], label="RPI Index")
    plt.title("CPI vs RPI Index")
    plt.xlabel("Date")
    plt.ylabel("Index")
    plt.legend()
    plt.grid(True)
    save_chart("07_cpi_vs_rpi.png")

    x = master["cpi_index"]
    y = master["e09000001_average_price"]

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y)

    if len(master) >= 2:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), label="Trendline")
        plt.legend()

    plt.title("Relationship Between CPI and Housing Prices")
    plt.xlabel("CPI Index")
    plt.ylabel("Average House Price (£)")
    plt.grid(True)
    save_chart("08_cpi_vs_housing_scatter.png")

    print("\nDashboard visuals created successfully.")


if __name__ == "__main__":
    main()
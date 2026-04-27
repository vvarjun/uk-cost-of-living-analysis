import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

housing = pd.read_csv(DATA_PROCESSED / "housing_merged_clean.csv")

housing["date"] = pd.to_datetime(
    housing["date"].astype(str).str.strip(),
    format="%b-%y",
    errors="coerce"
)

housing = housing.dropna(subset=["date"]).sort_values("date")

# Use City of London prices
df = housing[["date", "e09000001_average_price"]].dropna()

# Simple rolling forecast
df["rolling_mean"] = df["e09000001_average_price"].rolling(window=12).mean()

plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["e09000001_average_price"], label="Actual Price")
plt.plot(df["date"], df["rolling_mean"], label="12-Month Rolling Avg")

plt.title("Housing Price Trend with Rolling Forecast")
plt.xlabel("Date")
plt.ylabel("Price (£)")
plt.legend()
plt.grid(True)

output_path = PROJECT_ROOT / "outputs" / "figures" / "09_housing_forecast.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Saved: {output_path}")
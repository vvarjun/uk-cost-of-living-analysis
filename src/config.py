from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT_DIR / "data" / "raw"
DATA_PROCESSED = ROOT_DIR / "data" / "processed"
FIGURES_DIR = ROOT_DIR / "outputs" / "figures"
MODELS_DIR = ROOT_DIR / "outputs" / "models"

RAW_FILES = {
    "cost_of_living": "cost_of_living_index_2022.csv",
    "spareroom_listings": "spareroom_rental_listings_2023_04_16.csv",
    "headline_inflation": "headline_inflation_index.csv",
    "gdp_index": "gdp_index.csv",
    "food_price_index": "food_price_index.csv",
    "producer_price_index": "producer_price_index.csv",
    "average_house_prices": "average_house_prices_uk.csv",
    "housing_price_index": "housing_price_index_uk.csv",
    "property_sales_volume": "property_sales_volume_uk.csv",
    "spareroom_gdp_index": "spareroom_gdp_index.xlsx",
    "spareroom_gdp_index_secondary": "spareroom_gdp_index_secondary.xlsx",
    "cpi_reference_tables": "consumer_price_inflation_reference_tables.xlsx",
}

RANDOM_STATE = 42
TEST_SIZE = 0.2

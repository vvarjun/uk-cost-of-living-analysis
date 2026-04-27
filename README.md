# UK Cost of Living & CPI Analysis

A GitHub-ready analyst portfolio project that explores UK cost-of-living patterns using CPI, housing, GDP, food-price, producer-price, rental, and cost-of-living index datasets.

The project started as a dissertation notebook and has been refactored into a clean, reproducible analyst project with reusable Python scripts, a structured data folder, and a polished README.

## Project Objectives

- Analyse UK cost-of-living indicators across CPI, housing, rent, food, and macroeconomic data.
- Identify relationships between inflation indicators and cost-of-living components.
- Compare UK housing trends using average price, index, and sales-volume datasets.
- Build baseline machine-learning models for selected cost-of-living indicators.
- Present a clean project structure suitable for GitHub, recruiters, and analyst portfolios.

## Repository Structure

```text
uk-cost-of-living-analysis/
├── data/
│   ├── raw/                 # Included raw datasets
│   ├── processed/           # Generated cleaned datasets
│   └── README.md            # Data catalog and source notes
├── notebooks/
│   └── 01_cost_of_living_analysis.ipynb
├── outputs/
│   ├── figures/             # Exported charts
│   └── models/              # Saved models
├── src/
│   ├── config.py
│   ├── data_preprocessing.py
│   ├── eda.py
│   ├── modeling.py
│   ├── utils.py
│   └── validate_data.py
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

## Included Datasets

| Dataset | Project filename | Source |
|---|---|---|
| Cost of Living Index 2022 | `cost_of_living_index_2022.csv` | Numbeo |
| UK rental listings | `spareroom_rental_listings_2023_04_16.csv` | SpareRoom |
| Headline inflation index | `headline_inflation_index.csv` | IMF Data |
| GDP index | `gdp_index.csv` | IMF Data |
| Food price index | `food_price_index.csv` | IMF Data |
| Producer price index | `producer_price_index.csv` | IMF Data |
| Average UK house prices | `average_house_prices_uk.csv` | UK House Price Index / HM Land Registry |
| UK housing price index | `housing_price_index_uk.csv` | UK House Price Index / HM Land Registry |
| UK property sales volume | `property_sales_volume_uk.csv` | UK House Price Index / HM Land Registry |
| SpareRoom GDP support sheet | `spareroom_gdp_index.xlsx` | SpareRoom / supporting worksheet |
| SpareRoom GDP support sheet, secondary copy | `spareroom_gdp_index_secondary.xlsx` | SpareRoom / supporting worksheet |
| UK CPI detailed reference tables | `consumer_price_inflation_reference_tables.xlsx` | Office for National Statistics (ONS) |

Source references:

- ONS Consumer Price Inflation reference tables: measures of monthly UK inflation including CPIH, CPI, and RPI.
- UK House Price Index: HM Land Registry datasets for average price, index, and sales-volume indicators.
- SpareRoom statistics and rental index: UK room-rental market statistics and listing data.
- Numbeo Cost of Living Index 2022: country-level cost-of-living comparison data.
- IMF macroeconomic datasets: inflation, food consumer price inflation, producer price inflation, and GDP-related index indicators.

## Setup

```bash
git clone <your-repo-url>
cd uk-cost-of-living-analysis
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

### 1. Validate raw data

```bash
python src/validate_data.py
```

### 2. Run preprocessing

```bash
python src/data_preprocessing.py
```

### 3. Run EDA charts

```bash
python src/eda.py
```

### 4. Train baseline models

```bash
python src/modeling.py
```

### 5. Open the notebook

```bash
jupyter notebook notebooks/01_cost_of_living_analysis.ipynb
```

## Expected Outputs

After running the scripts, the project will generate:

- Cleaned datasets in `data/processed/`
- Charts in `outputs/figures/`
- Model files and metrics in `outputs/models/`

## Suggested Portfolio Talking Points

- Demonstrates data cleaning across CSV and Excel datasets.
- Combines macroeconomic, housing, rental, and CPI indicators.
- Uses reproducible scripts rather than a single messy notebook.
- Includes model evaluation and output folders for recruiter-friendly review.

## Notes Before Publishing

The raw datasets are included in this zip at the user's request. Before publishing the repository publicly, review each source's reuse terms and keep the source attribution in this README and `data/README.md`.

from __future__ import annotations

from config import DATA_RAW, RAW_FILES
from data_preprocessing import load_dataset


def validate_raw_data() -> None:
    print(f"Raw data folder: {DATA_RAW}")
    print(f"Expected datasets: {len(RAW_FILES)}")

    missing = []

    for key, filename in RAW_FILES.items():
        path = DATA_RAW / filename

        print("\n" + "=" * 80)
        print(f"{key}: {filename}")

        if not path.exists():
            print("Status: MISSING")
            missing.append(filename)
            continue

        try:
            df = load_dataset(key).head(5)

            print("Status: OK")
            print("Preview shape:", df.shape)
            print("Columns:", list(df.columns)[:12])

        except Exception as exc:
            print("Status: LOAD ERROR")
            print(exc)

    if missing:
        raise FileNotFoundError(f"Missing files: {missing}")

    print("\nAll configured raw datasets are present.")


if __name__ == "__main__":
    validate_raw_data()
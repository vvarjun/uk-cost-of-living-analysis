from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd


def ensure_dirs(paths: Iterable[Path]) -> None:
    """Create project directories if they do not already exist."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def clean_column_name(column: str) -> str:
    """Convert a column name to snake_case."""
    column = str(column).strip()
    column = re.sub(r"[^0-9a-zA-Z]+", "_", column)
    column = re.sub(r"_+", "_", column)
    return column.strip("_").lower()


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with clean snake_case column names."""
    out = df.copy()
    out.columns = [clean_column_name(col) for col in out.columns]
    return out


def coerce_numeric_columns(df: pd.DataFrame, exclude: Iterable[str] = ("date", "country")) -> pd.DataFrame:
    """Convert numeric-looking object columns to numeric values."""
    out = df.copy()
    exclude = set(exclude)
    for col in out.columns:
        if col in exclude:
            continue
        if out[col].dtype == "object":
            cleaned = out[col].astype(str).str.replace(",", "", regex=False).str.replace("£", "", regex=False)
            converted = pd.to_numeric(cleaned, errors="coerce")
            if converted.notna().sum() > 0:
                out[col] = converted
    return out


def save_figure(fig, path: Path) -> None:
    """Save a matplotlib figure with consistent settings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")

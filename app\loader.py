from __future__ import annotations

from pathlib import Path

import pandas as pd


DATE_COLUMNS = {
    "orders": ["order_date"],
    "users": ["register_date"],
    "marketing": ["date"],
    "reviews": ["review_date"],
}


def load_tables(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load CSV files from a folder as named tables."""
    tables: dict[str, pd.DataFrame] = {}
    for csv_path in sorted(data_dir.glob("*.csv")):
        name = csv_path.stem
        df = pd.read_csv(csv_path)
        for col in DATE_COLUMNS.get(name, []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        tables[name] = df
    return tables


def require_tables(tables: dict[str, pd.DataFrame], required: list[str]) -> None:
    missing = [name for name in required if name not in tables]
    if missing:
        raise ValueError(f"Missing required table(s): {', '.join(missing)}")


from __future__ import annotations

import pandas as pd


def profile_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for table_name, df in tables.items():
        for col in df.columns:
            rows.append(
                {
                    "table": table_name,
                    "column": col,
                    "dtype": str(df[col].dtype),
                    "rows": len(df),
                    "missing": int(df[col].isna().sum()),
                    "missing_rate": round(float(df[col].isna().mean()), 4),
                    "unique_values": int(df[col].nunique(dropna=True)),
                }
            )
    return pd.DataFrame(rows)


def table_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for table_name, df in tables.items():
        rows.append(
            {
                "table": table_name,
                "rows": len(df),
                "columns": len(df.columns),
                "duplicated_rows": int(df.duplicated().sum()),
                "missing_cells": int(df.isna().sum().sum()),
            }
        )
    return pd.DataFrame(rows)


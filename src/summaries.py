import pandas as pd
from typing import List

def summarize_numeric(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    if not numeric_cols:
        return pd.DataFrame()
    summary = df[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75]).T
    summary = summary.rename(columns={"25%": "p25", "50%": "median", "75%": "p75"})
    summary.insert(0, "column", summary.index)
    return summary.reset_index(drop=True)

def summarize_categorical(df: pd.DataFrame, cat_cols: List[str], top_k: int = 10):
    rows = []
    for c in cat_cols:
        s = df[c].astype("string")
        top = s.value_counts(dropna=True).head(top_k)
        rows.append({
            "column": c,
            "count": int(s.shape[0]),
            "missing": int(s.isna().sum()),
            "unique": int(s.nunique(dropna=True)),
            "top_values": "; ".join([f"{k} ({v})" for k, v in top.items()])
        })
    return pd.DataFrame(rows)

def missingness_table(df: pd.DataFrame) -> pd.DataFrame:
    return (
        pd.DataFrame({
            "column": df.columns.astype(str),
            "missing_rate": df.isna().mean().astype(float),
            "missing_count": df.isna().sum().astype(int)
        })
        .sort_values("missing_rate", ascending=False)
        .reset_index(drop=True)
    )

def correlations(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    if len(numeric_cols) < 2:
        return pd.DataFrame()
    return df[numeric_cols].corr()

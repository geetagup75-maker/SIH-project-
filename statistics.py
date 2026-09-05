import numpy as np
import pandas as pd


# =========================================================
# DESCRIPTIVE STATISTICS
# =========================================================

def descriptive_statistics(series):

    series = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    return {
        "count": len(series),
        "mean": series.mean(),
        "median": series.median(),
        "std": series.std(),
        "min": series.min(),
        "q1": series.quantile(0.25),
        "q3": series.quantile(0.75),
        "max": series.max()
    }


# =========================================================
# IQR
# =========================================================

def iqr_analysis(series):

    series = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = series[
        (series < lower) |
        (series > upper)
    ]

    return {
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "lower_bound": lower,
        "upper_bound": upper,
        "outlier_count": len(outliers)
    }


# =========================================================
# Z SCORE
# =========================================================

def calculate_z_score(series):

    series = pd.to_numeric(
        series,
        errors="coerce"
    )

    mean = series.mean()
    std = series.std()

    if std == 0:
        return pd.Series(
            np.zeros(len(series)),
            index=series.index
        )

    return (series - mean) / std


def zscore_analysis(series, threshold=3):

    z = calculate_z_score(series)

    outliers = z.abs() > threshold

    return {
        "z_scores": z,
        "outlier_count": outliers.sum()
    }


# =========================================================
# MAD
# =========================================================

def mad_analysis(series):

    series = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    median = series.median()

    mad = np.median(
        np.abs(series - median)
    )

    if mad == 0:
        return {
            "median": median,
            "MAD": 0,
            "outlier_count": 0
        }

    modified_z = (
        0.6745 *
        (series - median)
        / mad
    )

    outliers = modified_z.abs() > 3.5

    return {
        "median": median,
        "MAD": mad,
        "outlier_count": outliers.sum()
    }


# =========================================================
# COEFFICIENT OF VARIATION
# =========================================================

def coefficient_of_variation(series):

    series = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    mean = series.mean()
    std = series.std()

    if mean == 0:
        return np.nan

    return (
        std / mean
    ) * 100
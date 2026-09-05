import numpy as np
import pandas as pd


# =========================================================
# PRICE RELATIVE
# =========================================================

def price_relative(current_price, base_price):

    if base_price == 0:
        return np.nan

    return (current_price / base_price) * 100


# =========================================================
# LASPEYRES INDEX
# =========================================================

def laspeyres_index(
    current_prices,
    base_prices,
    base_quantities
):

    numerator = np.sum(
        current_prices * base_quantities
    )

    denominator = np.sum(
        base_prices * base_quantities
    )

    if denominator == 0:
        return np.nan

    return (numerator / denominator) * 100


# =========================================================
# PAASCHE INDEX
# =========================================================

def paasche_index(
    current_prices,
    base_prices,
    current_quantities
):

    numerator = np.sum(
        current_prices * current_quantities
    )

    denominator = np.sum(
        base_prices * current_quantities
    )

    if denominator == 0:
        return np.nan

    return (numerator / denominator) * 100


# =========================================================
# FISHER IDEAL INDEX
# =========================================================

def fisher_index(laspeyres, paasche):

    if (
        pd.isna(laspeyres)
        or pd.isna(paasche)
        or laspeyres < 0
        or paasche < 0
    ):
        return np.nan

    return np.sqrt(
        laspeyres * paasche
    )


# =========================================================
# WEIGHTED PRICE RELATIVE
# =========================================================

def weighted_price_relative(
    current_prices,
    base_prices,
    weights
):

    relatives = (
        current_prices /
        base_prices
    ) * 100

    weighted_index = np.average(
        relatives,
        weights=weights
    )

    return weighted_index


# =========================================================
# INDEX CHANGE
# =========================================================

def index_change(current_index, previous_index):

    if previous_index == 0:
        return np.nan

    return (
        (current_index - previous_index)
        / previous_index
    ) * 100


# =========================================================
# MONTH-ON-MONTH
# =========================================================

def mom_change(series):

    return series.pct_change() * 100


# =========================================================
# YEAR-ON-YEAR
# =========================================================

def yoy_change(series):

    return series.pct_change(12) * 100


# =========================================================
# PRICE RELATIVE SERIES
# =========================================================

def calculate_price_relatives(
    df,
    price_column="total_fare"
):

    df = df.copy()

    base_price = df[price_column].iloc[0]

    df["price_relative"] = (
        df[price_column] /
        base_price
    ) * 100

    return df
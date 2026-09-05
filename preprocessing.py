import pandas as pd
import numpy as np


def clean_fare_data(df):

    df = df.copy()

    # -----------------------------
    # Date conversion
    # -----------------------------

    df["departure_date"] = pd.to_datetime(
        df["departure_date"],
        errors="coerce"
    )

    df["booking_date"] = pd.to_datetime(
        df["booking_date"],
        errors="coerce"
    )

    df["scraped_at"] = pd.to_datetime(
        df["scraped_at"],
        errors="coerce"
    )

    # -----------------------------
    # Numeric conversion
    # -----------------------------

    numeric_columns = [
        "advance_days",
        "base_fare",
        "taxes",
        "convenience_fee",
        "total_fare"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # -----------------------------
    # String cleanup
    # -----------------------------

    string_columns = [
        "origin",
        "destination",
        "carrier_code",
        "carrier_name",
        "fare_class",
        "source"
    ]

    for col in string_columns:

        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
        )

    # -----------------------------
    # Route
    # -----------------------------

    df["route"] = (
        df["origin"].astype(str)
        + " → "
        + df["destination"].astype(str)
    )

    # -----------------------------
    # Month
    # -----------------------------

    df["month"] = df["departure_date"].dt.to_period("M").astype(str)

    # -----------------------------
    # Year
    # -----------------------------

    df["year"] = df["departure_date"].dt.year

    # -----------------------------
    # Month name
    # -----------------------------

    df["month_name"] = df["departure_date"].dt.month_name()

    # -----------------------------
    # Day of week
    # -----------------------------

    df["day_of_week"] = df["departure_date"].dt.day_name()

    # -----------------------------
    # Fare components
    # -----------------------------

    df["tax_percentage"] = np.where(
        df["total_fare"] > 0,
        df["taxes"] / df["total_fare"] * 100,
        np.nan
    )

    df["fee_percentage"] = np.where(
        df["total_fare"] > 0,
        df["convenience_fee"] / df["total_fare"] * 100,
        np.nan
    )

    return df


def remove_duplicates(df):

    df = df.copy()

    duplicate_columns = [
        "origin",
        "destination",
        "carrier_code",
        "departure_date",
        "booking_date",
        "fare_class",
        "source"
    ]

    existing = [
        col for col in duplicate_columns
        if col in df.columns
    ]

    before = len(df)

    df = df.drop_duplicates(subset=existing)

    after = len(df)

    return df, before - after


def missing_value_summary(df):

    summary = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_percentage":
            (df.isna().mean() * 100).round(2).values
    })

    return summary.sort_values(
        "missing_percentage",
        ascending=False
    )


def data_quality_summary(df):

    duplicate_count = df.duplicated().sum()

    missing_cells = df.isna().sum().sum()

    total_cells = df.shape[0] * df.shape[1]

    missing_percentage = (
        missing_cells / total_cells * 100
        if total_cells > 0 else 0
    )

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": duplicate_count,
        "missing_cells": missing_cells,
        "missing_percentage": missing_percentage
    }
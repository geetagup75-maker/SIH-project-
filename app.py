import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from textwrap import dedent

from database import (
    load_fare_records,
    load_index_values
)

from preprocessing import (
    clean_fare_data,
    remove_duplicates,
    missing_value_summary,
    data_quality_summary
)

from index_calculation import (
    price_relative,
    index_change,
    mom_change,
    yoy_change
)

from statistics import (
    descriptive_statistics,
    iqr_analysis,
    zscore_analysis,
    mad_analysis,
    coefficient_of_variation
)

from styles import load_css


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="India Airfare Price Index",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def get_data():

    fares = load_fare_records()
    index_values = load_index_values()

    fares = clean_fare_data(fares)

    return fares, index_values


fares, index_values = get_data()


# =========================================================
# REMOVE DUPLICATES
# =========================================================

fares, duplicate_count = remove_duplicates(fares)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def money(value):

    if pd.isna(value):
        return "N/A"

    return f"₹{value:,.0f}"


def number(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:,.0f}"


def percentage(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}%"


def kpi(title, value, subtitle=""):
    html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-subtitle">{subtitle}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def section(title):
    html = f'<div class="section-title">{title}</div>'
    st.markdown(html, unsafe_allow_html=True)


def insight(text):
    html = f'<div class="insight-card">{text}</div>'
    st.markdown(html, unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-header">'
    '<div class="dashboard-title">✈️ India Airfare Price Index</div>'
    '<div class="dashboard-subtitle">Real-time airfare intelligence for CPI augmentation</div>'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ✈️ Airfare Intelligence")

    st.markdown("---")

    navigation = st.radio(
        "Dashboard",
        [
            "Executive Overview",
            "Airfare Price Index",
            "Route Analysis",
            "Airline Analysis",
            "Statistical Analysis",
            "Time-Series Analysis",
            "Data Quality",
            "CPI Methodology"
        ]
    )

    st.markdown("---")

    st.markdown("### Global Filters")

    # Airline

    airlines = sorted(
        fares["carrier_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_airlines = st.multiselect(
        "Airline",
        airlines
    )

    # Route

    routes = sorted(
        fares["route"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_routes = st.multiselect(
        "Route",
        routes
    )

    # Origin

    origins = sorted(
        fares["origin"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_origins = st.multiselect(
        "Origin",
        origins
    )

    # Destination

    destinations = sorted(
        fares["destination"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_destinations = st.multiselect(
        "Destination",
        destinations
    )

    # Fare class

    fare_classes = sorted(
        fares["fare_class"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_fare_classes = st.multiselect(
        "Fare Class",
        fare_classes
    )

    # Source

    sources = sorted(
        fares["source"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_sources = st.multiselect(
        "Data Source",
        sources
    )

    # Advance days

    min_advance = int(
        fares["advance_days"].min()
    )

    max_advance = int(
        fares["advance_days"].max()
    )

    advance_range = st.slider(
        "Advance Booking Days",
        min_value=min_advance,
        max_value=max_advance,
        value=(min_advance, max_advance)
    )

    # Date

    min_date = fares["departure_date"].min()
    max_date = fares["departure_date"].max()

    date_range = st.date_input(
        "Departure Date",
        value=(min_date, max_date)
    )


# =========================================================
# GLOBAL FILTERING
# =========================================================

filtered_df = fares.copy()


if selected_airlines:

    filtered_df = filtered_df[
        filtered_df["carrier_name"].isin(
            selected_airlines
        )
    ]


if selected_routes:

    filtered_df = filtered_df[
        filtered_df["route"].isin(
            selected_routes
        )
    ]


if selected_origins:

    filtered_df = filtered_df[
        filtered_df["origin"].isin(
            selected_origins
        )
    ]


if selected_destinations:

    filtered_df = filtered_df[
        filtered_df["destination"].isin(
            selected_destinations
        )
    ]


if selected_fare_classes:

    filtered_df = filtered_df[
        filtered_df["fare_class"].isin(
            selected_fare_classes
        )
    ]


if selected_sources:

    filtered_df = filtered_df[
        filtered_df["source"].isin(
            selected_sources
        )
    ]


filtered_df = filtered_df[
    filtered_df["advance_days"].between(
        advance_range[0],
        advance_range[1]
    )
]


if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

    filtered_df = filtered_df[
        filtered_df["departure_date"].between(
            start_date,
            end_date
        )
    ]


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

def executive_overview():

    section("Executive Overview")

    if filtered_df.empty:

        st.warning(
            "No observations match the selected filters."
        )

        return

    avg_fare = filtered_df["total_fare"].mean()

    median_fare = filtered_df["total_fare"].median()

    routes_count = filtered_df["route"].nunique()

    airlines_count = filtered_df["carrier_name"].nunique()

    observations = len(filtered_df)

    cols = st.columns(5)

    with cols[0]:
        kpi(
            "Average Fare",
            money(avg_fare)
        )

    with cols[1]:
        kpi(
            "Median Fare",
            money(median_fare)
        )

    with cols[2]:
        kpi(
            "Routes",
            number(routes_count)
        )

    with cols[3]:
        kpi(
            "Airlines",
            number(airlines_count)
        )

    with cols[4]:
        kpi(
            "Observations",
            number(observations)
        )

    # -----------------------------------------------------
    # Daily airfare
    # -----------------------------------------------------

    section("Average Airfare Trend")

    daily = (
        filtered_df
        .groupby("departure_date")["total_fare"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        daily,
        x="departure_date",
        y="total_fare",
        markers=True,
        labels={
            "departure_date": "Departure Date",
            "total_fare": "Average Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # Top routes
    # -----------------------------------------------------

    section("Route Fare Intelligence")

    route_data = (
        filtered_df
        .groupby("route")
        .agg(
            average_fare=("total_fare", "mean"),
            observations=("id", "count")
        )
        .reset_index()
        .sort_values(
            "average_fare",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        route_data,
        x="average_fare",
        y="route",
        orientation="h",
        text="average_fare",
        labels={
            "average_fare": "Average Fare (₹)",
            "route": "Route"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# AIRFARE INDEX
# =========================================================

def airfare_index_page():

    section("Airfare Price Index")

    if index_values.empty:

        st.warning(
            "No index values are available."
        )

        return

    index_data = index_values.copy()

    index_data["date"] = pd.to_datetime(
        index_data["date"],
        errors="coerce"
    )

    index_data = index_data.sort_values(
        "date"
    )

    # -----------------------------------------------------
    # Latest index
    # -----------------------------------------------------

    latest = index_data.iloc[-1]

    previous = (
        index_data.iloc[-2]
        if len(index_data) > 1
        else None
    )

    latest_index = latest["index_value"]

    if previous is not None:

        change = index_change(
            latest_index,
            previous["index_value"]
        )

    else:

        change = np.nan

    cols = st.columns(4)

    with cols[0]:

        kpi(
            "Current Index",
            f"{latest_index:.2f}",
            "Base = 100"
        )

    with cols[1]:

        kpi(
            "Previous Index",
            f"{previous['index_value']:.2f}"
            if previous is not None
            else "N/A"
        )

    with cols[2]:

        kpi(
            "Change",
            percentage(change)
        )

    with cols[3]:

        kpi(
            "Base Value",
            f"{latest['base_value']:.2f}"
        )

    # -----------------------------------------------------
    # Index chart
    # -----------------------------------------------------

    section("Airfare Price Index Trend")

    fig = px.line(
        index_data,
        x="date",
        y="index_value",
        markers=True,
        labels={
            "date": "Date",
            "index_value": "Airfare Index"
        }
    )

    fig.add_hline(
        y=100,
        line_dash="dash",
        annotation_text="Base = 100"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # MoM / YoY
    # -----------------------------------------------------

    index_data["MoM %"] = (
        index_data["index_value"]
        .pct_change() * 100
    )

    index_data["YoY %"] = (
        index_data["index_value"]
        .pct_change(12) * 100
    )

    section("Index Changes")

    st.dataframe(
        index_data[
            [
                "date",
                "index_value",
                "MoM %",
                "YoY %",
                "period"
            ]
        ].sort_values(
            "date",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# ROUTE ANALYSIS
# =========================================================

def route_analysis_page():

    section("Route Analysis")

    if filtered_df.empty:

        st.warning("No data available.")

        return

    route_summary = (
        filtered_df
        .groupby("route")
        .agg(
            average_fare=("total_fare", "mean"),
            median_fare=("total_fare", "median"),
            minimum_fare=("total_fare", "min"),
            maximum_fare=("total_fare", "max"),
            observations=("id", "count")
        )
        .reset_index()
    )

    route_summary["range"] = (
        route_summary["maximum_fare"]
        - route_summary["minimum_fare"]
    )

    section("Route Fare Comparison")

    fig = px.bar(
        route_summary
        .sort_values(
            "average_fare",
            ascending=False
        )
        .head(15),
        x="route",
        y="average_fare",
        labels={
            "route": "Route",
            "average_fare": "Average Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section("Route Statistics")

    st.dataframe(
        route_summary.sort_values(
            "average_fare",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# AIRLINE ANALYSIS
# =========================================================

def airline_analysis_page():

    section("Airline Analysis")

    if filtered_df.empty:

        st.warning("No data available.")

        return

    airline_summary = (
        filtered_df
        .groupby("carrier_name")
        .agg(
            average_fare=("total_fare", "mean"),
            median_fare=("total_fare", "median"),
            minimum_fare=("total_fare", "min"),
            maximum_fare=("total_fare", "max"),
            observations=("id", "count")
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # Average fare
    # -----------------------------------------------------

    section("Average Fare by Airline")

    fig = px.bar(
        airline_summary.sort_values(
            "average_fare",
            ascending=False
        ),
        x="carrier_name",
        y="average_fare",
        labels={
            "carrier_name": "Airline",
            "average_fare": "Average Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # Fare distribution
    # -----------------------------------------------------

    section("Airline Fare Distribution")

    fig = px.box(
        filtered_df,
        x="carrier_name",
        y="total_fare",
        labels={
            "carrier_name": "Airline",
            "total_fare": "Total Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# STATISTICAL ANALYSIS
# =========================================================

def statistical_analysis_page():

    section("Statistical Analysis")

    if filtered_df.empty:

        st.warning("No data available.")

        return

    fares_series = filtered_df[
        "total_fare"
    ].dropna()

    stats = descriptive_statistics(
        fares_series
    )

    cols = st.columns(6)

    with cols[0]:
        kpi("Mean", money(stats["mean"]))

    with cols[1]:
        kpi("Median", money(stats["median"]))

    with cols[2]:
        kpi("Std. Dev.", money(stats["std"]))

    with cols[3]:
        kpi("Minimum", money(stats["min"]))

    with cols[4]:
        kpi("Q1", money(stats["q1"]))

    with cols[5]:
        kpi("Q3", money(stats["q3"]))

    # -----------------------------------------------------
    # Distribution
    # -----------------------------------------------------

    section("Fare Distribution")

    fig = px.histogram(
        filtered_df,
        x="total_fare",
        nbins=40,
        labels={
            "total_fare": "Total Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # IQR
    # -----------------------------------------------------

    section("IQR Outlier Detection")

    iqr = iqr_analysis(
        fares_series
    )

    cols = st.columns(4)

    with cols[0]:
        kpi(
            "Q1",
            money(iqr["Q1"])
        )

    with cols[1]:
        kpi(
            "Q3",
            money(iqr["Q3"])
        )

    with cols[2]:
        kpi(
            "IQR",
            money(iqr["IQR"])
        )

    with cols[3]:
        kpi(
            "Outliers",
            number(iqr["outlier_count"])
        )

    # -----------------------------------------------------
    # Z score
    # -----------------------------------------------------

    section("Z-Score Analysis")

    zscore = zscore_analysis(
        fares_series
    )

    kpi(
        "Z-Score Outliers",
        number(zscore["outlier_count"]),
        "Threshold = ±3"
    )

    # -----------------------------------------------------
    # MAD
    # -----------------------------------------------------

    section("Median Absolute Deviation")

    mad = mad_analysis(
        fares_series
    )

    cols = st.columns(3)

    with cols[0]:
        kpi(
            "Median",
            money(mad["median"])
        )

    with cols[1]:
        kpi(
            "MAD",
            money(mad["MAD"])
        )

    with cols[2]:
        kpi(
            "MAD Outliers",
            number(mad["outlier_count"])
        )

    # -----------------------------------------------------
    # CV
    # -----------------------------------------------------

    cv = coefficient_of_variation(
        fares_series
    )

    section("Fare Volatility")

    kpi(
        "Coefficient of Variation",
        percentage(cv),
        "CV = σ / μ × 100"
    )


# =========================================================
# TIME SERIES
# =========================================================

def time_series_page():

    section("Time-Series Analysis")

    if filtered_df.empty:

        st.warning("No data available.")

        return

    monthly = (
        filtered_df
        .groupby("month")
        .agg(
            average_fare=("total_fare", "mean"),
            median_fare=("total_fare", "median"),
            observations=("id", "count")
        )
        .reset_index()
    )

    monthly["month"] = pd.to_datetime(
        monthly["month"]
    )

    monthly["MoM %"] = (
        monthly["average_fare"]
        .pct_change() * 100
    )

    section("Monthly Average Fare")

    fig = px.line(
        monthly,
        x="month",
        y="average_fare",
        markers=True,
        labels={
            "month": "Month",
            "average_fare": "Average Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # Day of week
    # -----------------------------------------------------

    section("Fare Pattern by Day of Week")

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_data = (
        filtered_df
        .groupby("day_of_week")["total_fare"]
        .mean()
        .reindex(day_order)
        .reset_index()
    )

    fig = px.bar(
        day_data,
        x="day_of_week",
        y="total_fare",
        labels={
            "day_of_week": "Day",
            "total_fare": "Average Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # Advance purchase
    # -----------------------------------------------------

    section("Advance Booking vs Fare")

    advance_data = (
        filtered_df
        .groupby("advance_days")["total_fare"]
        .mean()
        .reset_index()
    )

    fig = px.scatter(
        advance_data,
        x="advance_days",
        y="total_fare",
        
        labels={
            "advance_days": "Advance Booking Days",
            "total_fare": "Average Fare (₹)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DATA QUALITY
# =========================================================

def data_quality_page():

    section("Data Quality & Coverage")

    quality = data_quality_summary(
        filtered_df
    )

    cols = st.columns(5)

    with cols[0]:
        kpi(
            "Rows",
            number(quality["rows"])
        )

    with cols[1]:
        kpi(
            "Columns",
            number(quality["columns"])
        )

    with cols[2]:
        kpi(
            "Duplicates",
            number(quality["duplicates"])
        )

    with cols[3]:
        kpi(
            "Missing Cells",
            number(quality["missing_cells"])
        )

    with cols[4]:
        kpi(
            "Missing %",
            percentage(
                quality["missing_percentage"]
            )
        )

    # -----------------------------------------------------
    # Missing values
    # -----------------------------------------------------

    section("Missing Value Analysis")

    missing = missing_value_summary(
        filtered_df
    )

    fig = px.bar(
        missing.head(15),
        x="missing_percentage",
        y="column",
        orientation="h",
        labels={
            "missing_percentage":
                "Missing Values (%)",
            "column": "Column"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # Source coverage
    # -----------------------------------------------------

    section("Data Source Coverage")

    source_data = (
        filtered_df
        .groupby("source")
        .size()
        .reset_index(
            name="observations"
        )
    )

    fig = px.pie(
        source_data,
        names="source",
        values="observations",
        hole=0.45
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CPI METHODOLOGY
# =========================================================

def cpi_methodology_page():

    section("CPI Methodology")

    st.markdown(
        """
        ### 1. Price Relative

        For an individual airfare:

        **Rₜ = (Pₜ / P₀) × 100**

        Where:

        - Pₜ = current-period airfare
        - P₀ = base-period airfare

        ---

        ### 2. Laspeyres Price Index ⭐

        **Lₜ = [Σ(PₜQ₀) / Σ(P₀Q₀)] × 100**

        The Laspeyres index keeps the base-period quantities fixed.

        This makes it particularly suitable for a CPI-style framework.

        ---

        ### 3. Paasche Price Index

        **Pₜ = [Σ(PₜQₜ) / Σ(P₀Qₜ)] × 100**

        The Paasche index uses current-period quantities.

        ---

        ### 4. Fisher Ideal Index ⭐

        **Fₜ = √(Lₜ × Pₜ)**

        Fisher combines the Laspeyres and Paasche indices.

        ---

        ### 5. Weighted Average ⭐

        Routes, airlines and fare products should not necessarily have
        equal importance.

        Weights should ideally represent passenger/travel volumes or
        another statistically justified measure.

        ---

        ### 6. Outlier Detection

        Three approaches are supported:

        **IQR**

        Q1, Q3 and:

        **IQR = Q3 − Q1**

        Lower bound:

        **Q1 − 1.5 × IQR**

        Upper bound:

        **Q3 + 1.5 × IQR**

        **Z-Score**

        **Z = (x − μ) / σ**

        **Median Absolute Deviation**

        A robust alternative for highly skewed airfare distributions.

        ---

        ### 7. Coefficient of Variation

        **CV = (σ / μ) × 100**

        Used to measure airfare volatility relative to its mean.

        ---

        ### 8. Time-Series Analysis

        The system evaluates:

        - Monthly airfare movement
        - MoM changes
        - YoY changes
        - Seasonal patterns
        - Day-of-week effects
        - Advance-booking effects
        - Sudden price movements

        ---

        ### Important methodological note

        The current `fare_records` table does not contain an explicit
        passenger-volume or quantity field (`Q₀` / `Qₜ`).

        Therefore, the dashboard does not invent quantity values.

        For an official CPI-augmentation index, the weighting framework
        should use an externally justified travel-volume source or an
        explicitly documented proxy.
        """
    )


# =========================================================
# NAVIGATION
# =========================================================

if navigation == "Executive Overview":

    executive_overview()

elif navigation == "Airfare Price Index":

    airfare_index_page()

elif navigation == "Route Analysis":

    route_analysis_page()

elif navigation == "Airline Analysis":

    airline_analysis_page()

elif navigation == "Statistical Analysis":

    statistical_analysis_page()

elif navigation == "Time-Series Analysis":

    time_series_page()

elif navigation == "Data Quality":

    data_quality_page()

elif navigation == "CPI Methodology":

    cpi_methodology_page()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'India Airfare Price Index | Real-time Airfare Intelligence | CPI Augmentation Research'
    '</div>',
    unsafe_allow_html=True
)
# ✈️ Real-Time Airfare Price Index for India

## Development of a Real-Time Airfare Price Index for India through Automated Collection of Airline and Online Travel Data for Augmentation of the Consumer Price Index (CPI)

---

## 📌 Project Overview

Airfare prices in India are highly dynamic and can change significantly depending on route, airline, booking window, travel date, fare class, and market conditions.

Traditional price statistics may not capture these short-term airfare movements with sufficient granularity or frequency.

This project aims to develop a **Real-Time Airfare Price Index for India** using automatically collected airfare data from airline and flight-data sources.

The system combines:

- Automated airfare data collection
- Data cleaning and standardization
- Statistical analysis
- Outlier detection
- Price-relative calculations
- Weighted index methodology
- Time-series analysis
- Route and airline-level analysis
- Interactive visualization
- CPI-oriented index methodology

The ultimate objective is to develop a **timely and granular airfare indicator that can complement existing CPI transport-price measurements**.

---

# 🎯 Objectives

The major objectives of the project are:

1. Collect airfare observations automatically from flight-data sources.

2. Capture important airfare dimensions such as:
   - Origin
   - Destination
   - Airline
   - Departure date
   - Booking date
   - Advance booking period
   - Base fare
   - Taxes
   - Convenience fee
   - Total fare
   - Fare class
   - Data source
   - Scraping timestamp

3. Clean and standardize the collected airfare data.

4. Identify and handle duplicate and anomalous observations.

5. Analyze airfare distributions and volatility.

6. Calculate price relatives and airfare price movements.

7. Develop a statistically justified weighted airfare price index.

8. Explore Laspeyres, Paasche and Fisher index methodologies.

9. Analyze route-level and airline-level airfare movements.

10. Study seasonal and time-series patterns in airfare prices.

11. Develop an interactive dashboard for monitoring airfare movements.

12. Investigate how the resulting airfare index could complement CPI-related transport price measurement.

---

# 🏗️ System Architecture

```text
                 FLIGHT DATA SOURCES
                         │
                         ▼
              Automated Data Collection
                         │
                         ▼
                  Raw Fare Records
                         │
                         ▼
                Data Preprocessing
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Duplicate Handling      Missing Values
              │                     │
              └──────────┬──────────┘
                         ▼
               Fare Standardization
                         │
                         ▼
                 Statistical Analysis
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           IQR        Z-Score       MAD
             │           │           │
             └───────────┼───────────┘
                         ▼
                  Price Relatives
                         │
                         ▼
                Weight Construction
                         │
                         ▼
             Airfare Price Index
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         Laspeyres    Paasche    Fisher
              │          │          │
              └──────────┼──────────┘
                         ▼
                National Index

Database Structure

The project uses SQLite for storing airfare observations and calculated index values.

fare_records
Column	Description
id	Unique record identifier
origin	Origin airport/city
destination	Destination airport/city
carrier_code	Airline code
carrier_name	Airline name
departure_date	Flight departure date
booking_date	Date on which fare was observed
advance_days	Days between booking and departure
base_fare	Base airfare
taxes	Taxes and statutory charges
convenience_fee	Convenience/service fee
total_fare	Total fare
fare_class	Fare booking class
source	Data source
scraped_at	Timestamp of data collection
index_values
Column	Description
id	Index record identifier
date	Index date
index_value	Calculated airfare index
period	Index period
base_value	Base-period value
📐 Statistical Methodology

The project uses several statistical and index-number methods.

1. Price Relative

For an individual airfare:

$$ R_t = \frac{P_t}{P_0}\times100 $$

Where:

\(P_t\) = current-period price
\(P_0\) = base-period price

A value of 100 represents the base-period price.

2. Laspeyres Price Index
$$ L_t = \frac{\sum P_tQ_0} {\sum P_0Q_0} \times100 $$

The Laspeyres index uses base-period quantities/weights.

It is particularly relevant to a CPI-style framework because the base-period expenditure structure can be kept fixed.

3. Paasche Price Index
$$ P_t = \frac{\sum P_tQ_t} {\sum P_0Q_t} \times100 $$

The Paasche index uses current-period quantities/weights.

4. Fisher Ideal Index
$$ F_t = \sqrt{L_tP_t} $$

The Fisher index combines the Laspeyres and Paasche indices and can reduce some of the bias associated with using only one weighting structure.

5. Weighted Average

Different routes, airlines and fare products should not necessarily contribute equally to the national index.

A weighting framework can incorporate measures such as:

Passenger volume
Route importance
Travel-market volume
Other statistically justified weights

The project aims to use externally justified travel-volume information where available rather than inventing passenger quantities.

🔎 Outlier Detection

Airfare data can contain extreme observations caused by unusual demand, data errors, scraping problems or temporary market conditions.

The project evaluates multiple outlier-detection approaches.

IQR Method
$$ IQR=Q_3-Q_1 $$

Lower bound:

$$ Q_1-1.5(IQR) $$

Upper bound:

$$ Q_3+1.5(IQR) $$
Z-Score
$$ Z=\frac{x-\mu}{\sigma} $$

Large absolute Z-scores can indicate unusually high or low observations.

Median Absolute Deviation

MAD provides a robust alternative when airfare distributions are highly skewed.

📈 Time-Series Analysis

The system analyzes airfare movement over time through:

Daily airfare trends
Monthly average fares
Month-over-month changes
Year-over-year changes
Day-of-week patterns
Advance-booking effects
Seasonal movements
Sudden airfare changes
Fare volatility
📊 Coefficient of Variation

Airfare volatility is evaluated using:

$$ CV=\frac{\sigma}{\mu}\times100 $$

A higher CV indicates greater variation relative to the average fare.

🖥️ Interactive Dashboard

The project includes a Streamlit-based analytical dashboard.

1. Executive Overview

Provides:

Average airfare
Median airfare
Number of routes
Number of airlines
Number of observations
Airfare trend
Route comparisons
2. Airfare Price Index

Provides:

Current index
Base value
Index trend
MoM movement
YoY movement
3. Route Analysis

Provides:

Average fare by route
Median fare
Minimum fare
Maximum fare
Fare range
Route-level comparisons
4. Airline Analysis

Provides:

Average fare by airline
Fare distribution
Airline comparisons
Airline-level observations
5. Statistical Analysis

Provides:

Mean
Median
Standard deviation
Quartiles
IQR
Z-score analysis
MAD analysis
Coefficient of Variation
6. Time-Series Analysis

Provides:

Monthly fare trends
Day-of-week patterns
Advance booking analysis
MoM changes
7. Data Quality

Provides:

Missing values
Duplicate observations
Missing percentage
Data-source coverage
8. CPI Methodology

Documents the statistical methodology used to construct and evaluate the airfare index.

🎛️ Dashboard Filters

The dashboard provides global filters for:

Airline
Route
Origin
Destination
Fare class
Data source
Advance booking days
Departure date

The sidebar remains available while navigating between dashboard sections.

🔄 Data Pipeline
Data Source
     ↓
Automated Collection
     ↓
Raw Airfare Data
     ↓
Validation
     ↓
Cleaning
     ↓
Duplicate Removal
     ↓
Standardization
     ↓
Outlier Detection
     ↓
Comparable Fare Products
     ↓
Weight Assignment
     ↓
Price Relative
     ↓
Index Calculation
     ↓
Validation
     ↓
Dashboard
🌐 Live Data Collection

The project is designed to acquire current flight-offer data through an authorized flight-data API.

The initial implementation uses the Amadeus Flight Offers Search API as a live data source.

The collected information is transformed into the project's standardized fare_records schema and stored in SQLite.

The system is designed so additional legitimate data sources can be incorporated in the future.

Note: API coverage may not represent every airline, fare type or market in India. Coverage limitations will therefore be documented when evaluating the final index.

🗂️ Project Structure
SIH/
│
├── app.py
│       # Streamlit dashboard
│       # All dashboard sections and charts
│
├── database.py
│       # SQLite database connection
│       # Data loading and insertion
│
├── preprocessing.py
│       # Data cleaning
│       # Duplicate handling
│       # Date and numeric conversion
│
├── index_calculation.py
│       # Price relatives
│       # Laspeyres
│       # Paasche
│       # Fisher
│       # Weighted calculations
│
├── statistics.py
│       # Descriptive statistics
│       # IQR
│       # Z-score
│       # MAD
│       # Coefficient of Variation
│
├── styles.py
│       # Dashboard styling
│
├── scraper.py
│       # Automated airfare data collection
│
├── test_scraper.py
│       # Scraper testing
│
├── airfare.db
│       # SQLite database
│
├── .env
│       # API credentials
│
├── .gitignore
│
└── README.md
🎯 Current Development Status

Completed

 SQLite database integration
 Fare-record data loading
 Data preprocessing
 Duplicate handling
 Basic statistical analysis
 IQR outlier analysis
 Z-score analysis
 MAD analysis
 Coefficient of Variation
 Route analysis
 Airline analysis
 Time-series visualization
 Data-quality dashboard
 Streamlit dashboard
 Global dashboard filters
 CPI methodology documentation
 Price-relative calculation framework

In Development

 Automated live airfare collection
 Scheduled data collection
 Fare-product standardization
 Robust outlier treatment pipeline
 Passenger-volume weighting
 Fully implemented Laspeyres index
 Fully implemented Paasche index
 Fisher Ideal Index
 National weighted airfare index
 Index validation
 CPI comparison
 Advanced seasonal analysis
 Final statistical validation

🛠️ Technologies Used

Programming
Python

Data Processing
Pandas
NumPy

Visualization
Plotly

Dashboard
Streamlit

Database
SQLite

Statistical Analysis
IQR
Z-score
Median Absolute Deviation
Coefficient of Variation
Index-number methodology

Data Acquisition
Flight-data API
Automated data collection pipeline

🚀 Installation

Clone the repository:

git clone <your-repository-url>
cd SIH

Install dependencies:

pip install -r requirements.txt

Create a .env file:

AMADEUS_CLIENT_ID=your_api_key
AMADEUS_CLIENT_SECRET=your_api_secret

Run the dashboard:

python -m streamlit run app.py
                         │
                         ▼
                  Streamlit Dashboard

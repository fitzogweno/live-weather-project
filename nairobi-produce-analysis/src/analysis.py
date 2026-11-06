
import pandas as pd
from pathlib import Path

# --------------------------------
# 1. SET PROJECT PATHS
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "nairobi_vegetable_prices.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------------
# 2. LOAD DATA
# --------------------------------

df = pd.read_csv(DATA_FILE)

df["date"] = pd.to_datetime(
    df["date"],
    dayfirst=True
)

print("DATA LOADED SUCCESSFULLY")
print("Dataset shape:", df.shape)

# --------------------------------
# 3. DATA QUALITY CHECKS
# --------------------------------

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATE RECORDS:")
print(df.duplicated(["date", "vegetable"]).sum())

# --------------------------------
# 4. CALCULATE DAILY PRICE CHANGES
# --------------------------------

df = df.sort_values(["vegetable", "date"])

df["daily_return"] = (
    df.groupby("vegetable")["price_kes_per_kg"]
    .pct_change()
)

# Convert daily return into percentage
df["daily_return_pct"] = df["daily_return"] * 100

# --------------------------------
# 5. OVERALL VOLATILITY
# --------------------------------

volatility = (
    df.groupby("vegetable")
    .agg(
        average_price=("price_kes_per_kg", "mean"),
        minimum_price=("price_kes_per_kg", "min"),
        maximum_price=("price_kes_per_kg", "max"),
        price_std=("price_kes_per_kg", "std"),
        daily_volatility=("daily_return", "std")
    )
    .reset_index()
)

# Express daily volatility as a percentage
volatility["daily_volatility_pct"] = (
    volatility["daily_volatility"] * 100
)

# Coefficient of variation of price levels
volatility["price_cv_pct"] = (
    volatility["price_std"] /
    volatility["average_price"]
) * 100

volatility = volatility.sort_values(
    "daily_volatility",
    ascending=False
)

# Save results
volatility.to_csv(
    OUTPUT_DIR / "vegetable_volatility.csv",
    index=False
)

print("\nOVERALL VOLATILITY RANKING:")
print(
    volatility[
        [
            "vegetable",
            "average_price",
            "daily_volatility_pct",
            "price_cv_pct"
        ]
    ].round(2).to_string(index=False)
)

# --------------------------------
# 6. MONTHLY VOLATILITY
# --------------------------------

df["month"] = df["date"].dt.to_period("M").astype(str)

monthly_volatility = (
    df.groupby(["vegetable", "month"])
    .agg(
        monthly_volatility=("daily_return", "std"),
        average_monthly_price=("price_kes_per_kg", "mean")
    )
    .reset_index()
)

monthly_volatility["monthly_volatility_pct"] = (
    monthly_volatility["monthly_volatility"] * 100
)

monthly_volatility.to_csv(
    OUTPUT_DIR / "monthly_volatility.csv",
    index=False
)

print("\nMONTHLY VOLATILITY:")
print(
    monthly_volatility[
        ["vegetable", "month", "monthly_volatility_pct"]
    ].round(2).to_string(index=False)
)

# --------------------------------
# 7. FIND MOST VOLATILE VEGETABLE
# --------------------------------

most_volatile = volatility.iloc[0]["vegetable"]

print("\nMOST VOLATILE VEGETABLE:")
print(most_volatile)

# --------------------------------
# 8. FIND ITS PEAK VOLATILITY MONTH
# --------------------------------

vegetable_months = monthly_volatility[
    monthly_volatility["vegetable"] == most_volatile
]

peak_month = vegetable_months.loc[
    vegetable_months["monthly_volatility"].idxmax()
]

print("\nPEAK VOLATILITY MONTH:")
print(peak_month["month"])

print(
    "Peak monthly volatility:",
    round(peak_month["monthly_volatility_pct"], 2),
    "%"
)

# --------------------------------
# 9. SAVE BUSINESS FINDING
# --------------------------------

finding = f"""
NAIROBI PRODUCE MARKET ANALYSIS

Analysis period: January to June 2026

Number of observations: {len(df)}

Most volatile vegetable: {most_volatile}

Peak volatility month: {peak_month['month']}

Peak monthly daily-return volatility:
{peak_month['monthly_volatility_pct']:.2f}%

Volatility is measured using the standard deviation
of daily percentage price changes.

This analysis uses generated sample data and should
not be interpreted as actual Nairobi market prices.
"""

finding_file = OUTPUT_DIR / "business_finding.txt"

finding_file.write_text(finding, encoding="utf-8")

print("\nBUSINESS FINDING:")
print(finding)

print("\nANALYSIS COMPLETED SUCCESSFULLY!")

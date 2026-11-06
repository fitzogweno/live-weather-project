
import pandas as pd
import numpy as np
from pathlib import Path

# Make results reproducible
np.random.seed(42)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Generate six months of daily dates
dates = pd.date_range(
    start="2026-01-01",
    end="2026-06-30",
    freq="D"
)

# Vegetable starting prices in Kenyan Shillings per kg
vegetables = {
    "Tomatoes": 80,
    "Onions": 120,
    "Potatoes": 65,
    "Cabbages": 45,
    "Carrots": 90
}

records = []

for vegetable, base_price in vegetables.items():

    # Different volatility for each vegetable
    volatility = {
        "Tomatoes": 0.14,
        "Onions": 0.07,
        "Potatoes": 0.05,
        "Cabbages": 0.09,
        "Carrots": 0.08
    }

    price = base_price

    for i, date in enumerate(dates):

        # Random daily price movement
        daily_change = np.random.normal(
            loc=0.001,
            scale=volatility[vegetable]
        )

        # Seasonal price variation
        seasonal_effect = 1 + 0.10 * np.sin(
            2 * np.pi * i / 90
        )

        # Introduce occasional market price spikes
        spike = 1

        if vegetable == "Tomatoes" and 90 <= i <= 120:
            spike = 1.25

        if vegetable == "Cabbages" and 140 <= i <= 155:
            spike = 1.15

        price = price * (1 + daily_change)

        # Keep prices within a realistic positive range
        price = max(price, base_price * 0.45)

        final_price = price * seasonal_effect * spike

        records.append({
            "date": date,
            "vegetable": vegetable,
            "price_kes_per_kg": round(final_price, 2)
        })

# Create DataFrame
df = pd.DataFrame(records)

# Sort records
df = df.sort_values(
    by=["date", "vegetable"]
).reset_index(drop=True)

# Save CSV
output_file = DATA_DIR / "nairobi_vegetable_prices.csv"

df.to_csv(output_file, index=False)

print("Dataset generated successfully!")
print(f"Saved to: {output_file}")
print("\nDataset preview:")
print(df.head(10))

print("\nDataset information:")
print(df.info())

print("\nNumber of records:", len(df))
print("\nVegetables:", df["vegetable"].unique())

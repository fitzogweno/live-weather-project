
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Make results reproducible
np.random.seed(42)

# 2. Generate 18 months of daily dates
dates = pd.date_range(
    start="2025-05-01",
    end="2026-10-30",
    freq="D"
)

# 3. Create seasonal transaction patterns
monthly_factors = {
    1: 1.00,
    2: 0.78,  # Lower transactions in February
    3: 0.95,
    4: 0.97,
    5: 1.00,
    6: 1.02,
    7: 1.03,
    8: 1.04,
    9: 1.05,
    10: 1.08,
    11: 1.12,
    12: 1.35  # Higher transactions in December
}

seasonality = np.array([
    monthly_factors[date.month] for date in dates
])

# 4. Add weekday patterns
weekday_factors = np.array([
    0.85,  # Monday
    0.90,  # Tuesday
    0.95,  # Wednesday
    1.00,  # Thursday
    1.15,  # Friday
    1.30,  # Saturday
    1.20   # Sunday
])

weekday_effect = weekday_factors[dates.dayofweek]

# 5. Add gradual business growth
growth = np.linspace(1.0, 1.15, len(dates))

# 6. Generate realistic daily transaction counts
base_transactions = 1000

expected_transactions = (
    base_transactions
    * seasonality
    * weekday_effect
    * growth
)

noise = np.random.normal(
    loc=1.0,
    scale=0.08,
    size=len(dates)
)

transactions = np.maximum(
    0,
    np.round(expected_transactions * noise)
).astype(int)

# 7. Create a DataFrame
df = pd.DataFrame({
    "Date": dates,
    "Transactions": transactions
})

df.set_index("Date", inplace=True)

# 8. Calculate monthly transaction totals
monthly_totals = df["Transactions"].resample("ME").sum()

# 9. Calculate the 30-day rolling average
rolling_average = df["Transactions"].rolling(
    window=30
).mean()

# 10. Create the chart
fig, ax1 = plt.subplots(figsize=(14, 7))

# Monthly transaction bars
ax1.bar(
    monthly_totals.index,
    monthly_totals.values,
    width=20,
    color="skyblue",
    label="Monthly Transactions"
)

ax1.set_xlabel("Month", fontsize=12)
ax1.set_ylabel("Total Monthly Transactions", fontsize=12)

# Add a second axis for the daily rolling average
ax2 = ax1.twinx()

ax2.plot(
    rolling_average.index,
    rolling_average.values,
    color="red",
    linewidth=2,
    label="30-Day Rolling Average"
)

ax2.set_ylabel("Average Daily Transactions", fontsize=12)

# 11. Add title and formatting
plt.title(
    "Nairobi Supermarket: Monthly Transaction Trends",
    fontsize=16,
    fontweight="bold"
)

ax1.grid(axis="y", linestyle="--", alpha=0.4)

# Combine both legends
bars, labels1 = ax1.get_legend_handles_labels()
lines, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    bars + lines,
    labels1 + labels2,
    loc="upper left"
)

fig.autofmt_xdate()
plt.tight_layout()

# 12. Save the chart as a PNG
plt.savefig(
    "monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

# 13. Display the chart
plt.show()

print("Analysis completed successfully!")
print("Chart saved as monthly_sales_trend.png")
print("\nMonthly transaction totals:")
print(monthly_totals)

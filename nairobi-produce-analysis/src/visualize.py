
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------
# 1. PROJECT PATHS
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "nairobi_vegetable_prices.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------
# 2. LOAD DATA
# --------------------------------

df = pd.read_csv(DATA_FILE)

df["date"] = pd.to_datetime(
    df["date"],
    dayfirst=True
)

volatility = pd.read_csv(
    OUTPUT_DIR / "vegetable_volatility.csv"
)

monthly = pd.read_csv(
    OUTPUT_DIR / "monthly_volatility.csv"
)

sns.set_theme(style="whitegrid", palette="Set2")

# --------------------------------
# 3. INDIVIDUAL PRICE TREND CHARTS
# --------------------------------

vegetables = sorted(df["vegetable"].unique())

for vegetable in vegetables:

    subset = df[df["vegetable"] == vegetable]

    plt.figure(figsize=(12, 5))

    sns.lineplot(
        data=subset,
        x="date",
        y="price_kes_per_kg",
        color="forestgreen",
        linewidth=1.5
    )

    plt.title(
        f"{vegetable} Daily Price Trend",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Date")
    plt.ylabel("Price (KES per kg)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    filename = f"{vegetable.lower()}_price_trend.png"

    plt.savefig(
        CHART_DIR / filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

# --------------------------------
# 4. COMBINED VEGETABLE PRICE CHART
# --------------------------------

plt.figure(figsize=(14, 7))

sns.lineplot(
    data=df,
    x="date",
    y="price_kes_per_kg",
    hue="vegetable",
    linewidth=1.5
)

plt.title(
    "Nairobi Vegetable Price Trends",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Date")
plt.ylabel("Price (KES per kg)")

plt.legend(title="Vegetable")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "combined_price_trends.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------
# 5. OVERALL VOLATILITY CHART
# --------------------------------

volatility = volatility.sort_values(
    "daily_volatility_pct",
    ascending=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=volatility,
    x="vegetable",
    y="daily_volatility_pct",
    hue="vegetable",
    legend=False
)

plt.title(
    "Daily Price Volatility by Vegetable",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Vegetable")
plt.ylabel("Daily Volatility (%)")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "overall_volatility.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------
# 6. MONTHLY VOLATILITY HEATMAP
# --------------------------------

pivot_data = monthly.pivot(
    index="vegetable",
    columns="month",
    values="monthly_volatility_pct"
)

plt.figure(figsize=(12, 6))

sns.heatmap(
    pivot_data,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    linewidths=0.5
)

plt.title(
    "Monthly Vegetable Price Volatility (%)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Vegetable")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "monthly_volatility_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------
# 7. COMPLETION MESSAGE
# --------------------------------

print("ALL CHARTS GENERATED SUCCESSFULLY!")

print("\nCharts saved in:")
print(CHART_DIR)

print("\nGenerated charts:")

for chart in sorted(CHART_DIR.glob("*.png")):
    print(chart.name)

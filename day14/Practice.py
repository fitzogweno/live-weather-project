import pandas as pd
import matplotlib.pyplot as plt

# Load and combine two months of data (from Day 14 pattern)
august = pd.read_csv("sales_august.csv")
september = pd.read_csv("sales_september.csv")
august["month"] = "August"
september["month"] = "September"
df = pd.concat([august, september], ignore_index=True)
df["revenue"] = df["quantity"] * df["price"]
print(f"Combined: {len(df)} rows | Total revenue: KES {df['revenue'].sum():,.0f}")
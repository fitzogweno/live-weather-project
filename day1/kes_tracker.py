# ============================================================
# BUILD PLAN
# ============================================================
# PROBLEM: A Kenyan business needs to quickly convert a KES quote
#          into USD, EUR, and GBP for international clients.
# INPUT:   A price in Kenyan Shillings (KES), entered by the user.
# PROCESSING: ExchangeRate-API v6, base=KES. Extract USD/EUR/GBP rates.
# OUTPUT:  Formatted line with all three converted amounts.
# ============================================================

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6"


def get_rates(base_currency="KES"):
    """Fetch conversion rates for KES from ExchangeRate-API."""
    url = f"{BASE_URL}/{API_KEY}/latest/{base_currency}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting API: {e}")
        sys.exit(1)

    if data.get("result") != "success":
        print(f"API error: {data.get('error-type', 'Unknown error')}")
        sys.exit(1)

    return data["conversion_rates"]


def convert(amount_kes, rates):
    """Convert KES to USD, EUR, and GBP and print the result."""
    targets = {"USD": rates["USD"], "EUR": rates["EUR"], "GBP": rates["GBP"]}
    print(f"\nKES {amount_kes:,.2f} is approximately:")
    for currency, rate in targets.items():
        converted = amount_kes * rate
        print(f"  {currency}: {converted:,.2f}")
    print()


def main():
    if not API_KEY:
        print("Error: EXCHANGE_RATE_API_KEY not found in .env file.")
        sys.exit(1)

    print("=== Kenyan Business Currency Tracker ===")
    try:
        raw = input("Enter amount in KES: ").strip().replace(",", "")
        amount = float(raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Error: Please enter a valid positive number.")
        sys.exit(1)

    rates = get_rates("KES")
    convert(amount, rates)


if __name__ == "__main__":
    main()
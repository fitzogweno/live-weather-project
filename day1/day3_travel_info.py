
import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    """Fetch current weather for a city."""
    if not API_KEY:
        print("Error: OpenWeatherMap API key not found.")
        print("Add OPENWEATHER_API_KEY to your .env file.")
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            url,
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=10,
        )

        if response.status_code == 404:
            print(f"Sorry, we couldn't find the city '{city}'.")
            print("Check the spelling and try again.")
            return None

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"Could not retrieve weather: {error}")
        return None


def get_country_info(country_code):
    """Fetch country information using its country code."""
    url = f"https://restcountries.com/v3.1/alpha/{country_code}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(
                "Note: Country information is temporarily unavailable."
            )
            return None

        data = response.json()

        if isinstance(data, list) and data:
            return data[0]

        print("Note: The country API returned an unexpected response.")
        return None

    except (requests.RequestException, ValueError):
        print("Note: Could not retrieve country information.")
        return None


def save_to_file(data, filename="travel_info.json"):
    """Save the combined results to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"\nYour results have been saved to {filename}.")
        return True

    except (OSError, TypeError) as error:
        print(f"Could not save the results: {error}")
        return False


def display_results(data):
    """Display a readable weather and country summary."""
    weather = data["weather"]
    country = data["country_info"]

    main = weather.get("main", {})
    conditions = weather.get("weather", [{}])[0]
    wind = weather.get("wind", {})

    print("\n" + "=" * 40)
    print(f"TRAVEL WEATHER REPORT: {data['city'].title()}")
    print("=" * 40)

    print("\nWEATHER")
    print("-" * 40)
    print(f"Temperature : {main.get('temp', 'N/A')} °C")
    print(
        f"Conditions  : "
        f"{conditions.get('description', 'N/A').title()}"
    )
    print(f"Feels like  : {main.get('feels_like', 'N/A')} °C")
    print(f"Humidity    : {main.get('humidity', 'N/A')}%")
    print(f"Wind speed  : {wind.get('speed', 'N/A')} m/s")

    if country:
        name = country.get("name", {}).get("common", "N/A")
        region = country.get("region", "N/A")
        population = country.get("population", 0)

        currencies_data = country.get("currencies", {})
        currency_names = [
            details.get("name", code)
            for code, details in currencies_data.items()
        ]
        currencies = ", ".join(currency_names) or "N/A"

        print("\nCOUNTRY INFORMATION")
        print("-" * 40)
        print(f"Country     : {name}")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}")
        print(f"Currency    : {currencies}")
    else:
        print("\nCountry information is unavailable.")

    print("\n" + "=" * 40)


def run_tool():
    """Collect input, call APIs, combine results, and save them."""
    print("\nWelcome to the Travel Weather Tool!")
    print("Get weather and country information for your destination.")

    city = input("\nEnter a city name: ").strip()

    if not city:
        print("No city entered. Please try again.")
        return

    print(f"\nLooking up information for {city.title()}...")

    weather_data = get_weather(city)

    if weather_data is None:
        print("No report was generated. Please try again.")
        return

    country_code = weather_data.get("sys", {}).get("country")

    country_data = None
    if country_code:
        country_data = get_country_info(country_code)

    # Combine both API responses into one data structure.
    results = {
        "city": weather_data.get("name", city),
        "country_code": country_code,
        "weather": weather_data,
        "country_info": country_data,
    }

    display_results(results)
    save_to_file(results)


if __name__ == "__main__":
    run_tool()
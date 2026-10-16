import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Nairobi, Kenya coordinates
LATITUDE = -20.01816
LONGITUDE = 57.58015

URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&current=temperature_2m,apparent_temperature,"
    "wind_speed_10m,weather_code"
    "&timezone=auto"
)

# Convert weather codes into human-readable descriptions
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Foggy with frost",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
}


def get_weather():
    """Fetch live weather data and print a readable report."""
    try:
        with urlopen(URL, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data["current"]
        units = data["current_units"]

        temperature = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]
        observed_at = current["time"]

        description = WEATHER_CODES.get(
            weather_code, "Weather description unavailable"
        )

        print("=" * 38)
        print("         LIVE WEATHER REPORT")
        print("=" * 38)
        print("Location:       Grand Baie, Mauritius")
        print(f"Observed at:    {observed_at}")
        print(f"Temperature:    {temperature:.1f}{units['temperature_2m']}")
        print(f"Feels like:     {feels_like:.1f}{units['apparent_temperature']}")
        print(f"Wind speed:     {wind_speed:.1f} {units['wind_speed_10m']}")
        print(f"Conditions:     {description}")
        print("=" * 38)
        print("Weather data retrieved successfully!")

    except (HTTPError, URLError, TimeoutError) as error:
        print(f"Could not retrieve weather data: {error}")
    except (KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"Could not process the weather data: {error}")


if __name__ == "__main__":
    get_weather()
OpenWeatherMap API Exercise
Overview

This project uses Python to retrieve current weather data from the OpenWeatherMap API.

It demonstrates how to:

Call an authenticated API using an API key.
Load credentials securely from a .env file.
Exclude sensitive files using .gitignore.
Handle HTTP errors such as invalid API keys, missing cities, and rate limits.
Display weather information in a readable format.
Requirements
Python 3
An OpenWeatherMap API key
The requests and python-dotenv packages
Setup
Clone or download this repository.
Install the required packages:

python -m pip install requests python-dotenv

Create a .env file in the project folder containing:

OPENWEATHER_API_KEY=your_actual_api_key_here

Replace the placeholder with your own API key. Never publish your real key.
Run the script

Run:

python day2_weather.py

The script retrieves weather information for Nairobi and prints the temperature, conditions, and humidity.

Security

The .env file is excluded using .gitignore. Never commit API keys or other secrets to GitHub.
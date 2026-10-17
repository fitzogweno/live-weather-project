## Kenyan Business Currency Tracker 💱

A Python command-line tool that converts a price in Kenyan Shillings (KES) to USD, EUR, and GBP using live exchange rates from ExchangeRate-API. Built for Kenyan businesses quoting international clients.

## Setup

1. Clone the repo
2. Install dependencies:
   pip install requests python-dotenv
3. Create a `.env` file in the project root with:
   EXCHANGE_RATE_API_KEY=your_key_here
4. Get a free API key at exchangerate-api.com

## Usage

python day1/kes_tracker.py

## Example Output

=== Kenyan Business Currency Tracker ===
Enter amount in KES: 100000

KES 100,000.00 is approximately:
  USD: 770.50
  EUR: 685.30
  GBP: 578.50

---
Travel Weather Tool 🌦️
Overview
The Travel Weather Tool is a Python command-line application that helps travellers learn about a destination before visiting.

It asks the user to enter a city name, retrieves live weather data from OpenWeatherMap, and fetches country information from the REST Countries API. It combines the responses into a single report and saves the results as a JSON file.

Problem It Solves
Travellers often need to check weather conditions and basic country information separately when planning a trip. This tool brings those details together in one simple command-line application.

Features
Accepts a city name from the user.
Retrieves current weather conditions and temperature.
Fetches country information, including region, population, and currency.
Combines data from two APIs.
Displays results in a readable format.
Saves the combined response to travel_info.json.
Handles invalid city names, network errors, and unavailable country information.
Technologies Used
Python
Requests
python-dotenv
OpenWeatherMap API
REST Countries API
Requirements
Python 3.10 or newer
An OpenWeatherMap API key
An internet connection
Installation and Setup
Clone this repository or download the project.
Open a terminal in the project directory.
Install the required packages:
   python -m pip install requests python-dotenv
Create a .env file in the project root and add your API key:
   OPENWEATHER_API_KEY=your_actual_api_key
Run the application:
   python day3_travel_info.py
Enter a city name when prompted.
Example
Welcome to the Travel Weather Tool!
Get weather and country information for your destination.

Enter a city name: Nairobi
The application displays the weather report and country details, then saves the combined data to travel_info.json.

Weather results depend on the live API response and may vary.

APIs Used
OpenWeatherMap Current Weather API
REST Countries API
Error Handling
The application handles missing API keys, invalid city names, failed network requests, unavailable country information, and file-writing errors.

Future Improvements
Support multiple destinations in one session.
Add a weather forecast.
Include travel recommendations based on weather conditions.
Add automated tests.
Author
Created as a Python API integration exercise.
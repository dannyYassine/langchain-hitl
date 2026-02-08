"""
Weather tools for the agent.

This module contains utility functions for retrieving weather information
using the Open-Meteo API (free, no API key required). These tools are used
by the LangChain agent to answer weather-related queries.
"""

import requests


def get_canadian_weather(city: str) -> dict:
    """
    Only use for canadian weather for a given city using Open-Meteo API (free, no API key required).
    """
    # Placeholder implementation - replace with actual file search logic
    return get_weather(city)


def get_weather(city: str) -> dict:
    """
    Only use to United states (US) weather for a given city using Open-Meteo API (free, no API key required).

    Args:
        city: Name of the city to get weather for

    Returns:
        Dictionary with weather information or error message
    """
    try:
        # First, geocode the city name
        geocode_url = (
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        )
        geo_response = requests.get(geocode_url, timeout=10)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {"error": f"City {city} not found"}

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # Get weather data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
        weather_response = requests.get(weather_url, timeout=10)
        weather_data = weather_response.json()

        return weather_data
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}

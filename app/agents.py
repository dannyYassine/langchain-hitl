from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy
import requests

"""
Agent module for weather information retrieval.

This module creates and configures a LangChain agent that can answer weather-related
queries using the GPT-5-mini model. The agent is equipped with a weather tool and
can process user messages to provide weather information.

Note: The model name "gpt-5-mini" appears to be a placeholder. As of the latest
information available, GPT-5 has not been released. Verify the correct model name
(e.g., "gpt-4", "gpt-3.5-turbo") before deployment.
"""

class WeatherResponse(BaseModel):
    city: str = Field(description="The city for which the weather information is provided")
    weather: str = Field(description="The weather information for the specified city")
    temperature: str = Field(description="The temperature in the specified city in celsius")

def get_weather(city: str) -> dict:
    """
    Get weather for a given city using Open-Meteo API (free, no API key required).
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Dictionary with weather information or error message
    """
    try:
        # First, geocode the city name
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
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

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
    response_format=ToolStrategy(WeatherResponse)
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in Montreal?"}]}
)
weatherResponse = response["structured_response"]

print(weatherResponse)
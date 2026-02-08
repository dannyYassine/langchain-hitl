"""
Pydantic model for weather responses.

This module contains the WeatherResponse model used for structured output
from the weather agent. It defines the schema for weather information including
city, weather conditions, temperature, and summary.
"""

from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    city: str = Field(
        description="The city for which the weather information is provided"
    )
    weather: str = Field(description="The weather information for the specified city")
    temperature: str = Field(
        description="The temperature in the specified city in celsius"
    )
    summary: str = Field(
        description="A summary of the weather conditions in the specified city"
    )

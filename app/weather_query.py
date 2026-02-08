"""Weather query request model."""

from pydantic import BaseModel, Field


class WeatherQuery(BaseModel):
    """User's weather query request."""

    query: str = Field(description="User's weather question")

import os

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from agent_factory import create_weather_agent
from weather_response import WeatherResponse

app = FastAPI(title="LangChain HITL")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "LangChain Human-in-the-Loop API"}


class WeatherQuery(BaseModel):
    query: str = Field(description="User's weather question")


@app.post(
    "/weather",
    response_model=WeatherResponse,
    description="Get weather information using AI agent",
)
async def get_weather_info(query: WeatherQuery):
    """
    Process weather query using LangChain agent.

    Args:
        query: User's weather question

    Returns:
        WeatherResponse with structured weather data

    Raises:
        HTTPException: If agent processing fails
    """
    try:
        agent = create_weather_agent()
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query.query}]}
        )
        return response["structured_response"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing failed: {str(e)}",
        )

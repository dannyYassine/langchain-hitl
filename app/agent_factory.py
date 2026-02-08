"""
Agent factory module for creating configured LangChain agents.

This module contains factory functions for creating agents with specific
configurations, middleware, and tools. It encapsulates agent creation logic
to promote reusability and separation of concerns.
"""

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
)
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

from weather_response import WeatherResponse
from tools import get_weather, get_canadian_weather


def create_weather_agent():
    """
    Create a weather agent with configured middleware and structured output.

    This function creates a LangChain agent configured to answer weather queries
    using GPT-4o-mini model. The agent includes:
    - Weather tool for fetching weather information
    - Model call limits (10 per thread, 5 per run)
    - Tool call limits (20 per thread, 10 per run)
    - Structured output format (WeatherResponse)

    Returns:
        Agent: Configured LangChain agent ready to process weather queries
    """
    agent = create_agent(
        model="gpt-5-mini",
        tools=[get_weather, get_canadian_weather],
        system_prompt="You are a helpful assistant",
        response_format=ToolStrategy(WeatherResponse),
        middleware=[
            ModelCallLimitMiddleware(
                thread_limit=10,
                run_limit=5,
                exit_behavior="end",
            ),
            ToolCallLimitMiddleware(thread_limit=20, run_limit=10),
            HumanInTheLoopMiddleware(
                interrupt_on={"get_weather": False, "get_canadian_weather": True},
                description_prefix="Tool execution pending approval",
            ),
        ],
        checkpointer=InMemorySaver(),
    )
    return agent

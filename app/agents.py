from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy

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

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

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
"""
Command-line interface for the weather agent.

This module provides an interactive CLI for querying weather information
using the configured LangChain weather agent. Users can ask about weather
in any city and receive structured responses.
"""

from agent_factory import create_weather_agent


if __name__ == "__main__":
    # Initialize the weather agent
    agent = create_weather_agent()

    # Run the agent in an interactive loop
    print("Weather Agent - Ask about weather in any city!")
    print("Type 'exit' or 'quit' to stop\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit", ""]:
            print("Goodbye!")
            break

        print("\n--- Processing your request ---")
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        weatherResponse = response["structured_response"]
        print(f"\nAgent: {weatherResponse.summary}\n")

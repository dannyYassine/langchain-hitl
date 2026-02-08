"""
Command-line interface for the weather agent.

This module provides an interactive CLI for querying weather information
using the configured LangChain weather agent. Users can ask about weather
in any city and receive structured responses.
"""

import json
from langgraph.types import Command

from agent_factory import create_weather_agent


def handle_interrupt(interrupt_data: list) -> tuple[list[dict], bool]:
    """
    Handle human-in-the-loop interrupt requests.

    Returns:
        Tuple of (decisions list, should_continue bool)
        - should_continue is False if user rejects, stopping the agent loop
    """
    decisions = []
    should_continue = True

    for interrupt in interrupt_data:
        value = interrupt.value
        actions = value["action_requests"]

        for action in actions:
            tool_name = action.get("name", "unknown")

            if tool_name == "get_canadian_weather":
                print(f"⚠️  This tool requires approval: {tool_name}")
                print("Sending notification to user for approval...")

            tool_args = action.get("args", action.get("arguments", {}))

            print(f"\n⚠️  Approval needed: {tool_name}({tool_args})")

            choice = input("Decision [a]pprove / [e]dit / [r]eject: ").strip().lower()

            if choice in ["a", "approve"]:
                decisions.append({"type": "approve"})
                print("✅ Approved")

            elif choice in ["e", "edit"]:
                print(f"Current args: {json.dumps(tool_args)}")
                new_args_str = input("New args (JSON): ").strip()
                try:
                    new_args = json.loads(new_args_str)
                    decisions.append({"type": "edit", "arguments": new_args})
                    print("✏️ Edited")
                except json.JSONDecodeError:
                    print("❌ Invalid JSON, using approve instead")
                    decisions.append({"type": "approve"})

            elif choice in ["r", "reject"]:
                feedback = input("Why reject? ").strip() or "User rejected this action"
                decisions.append({"type": "reject", "feedback": feedback})
                should_continue = False
                print("❌ Rejected - please rephrase your request")

            else:
                print("❌ Invalid choice, approving by default")
                decisions.append({"type": "approve"})

    return decisions, should_continue


if __name__ == "__main__":
    agent = create_weather_agent()

    print("Weather Agent - Ask about weather in any city!")
    print("Type 'exit' or 'quit' to stop\n")

    thread_id = "weather_cli_session"

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit", ""]:
            print("Goodbye!")
            break

        config = {"configurable": {"thread_id": thread_id}}
        response = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}, config=config
        )

        # Handle interrupts
        if "__interrupt__" in response:
            decisions, should_continue = handle_interrupt(response["__interrupt__"])

            # Always send decisions to agent to properly update state
            response = agent.invoke(
                Command(resume={"decisions": decisions}), config=config
            )

            if not should_continue:
                # User rejected - skip displaying result and wait for new input
                continue

        # Display result
        if (
            "structured_response" in response
            and response["structured_response"] is not None
        ):
            print(f"\nAgent: {response['structured_response'].summary}\n")
        else:
            last_message = response["messages"][-1] if response["messages"] else None
            if last_message:
                print(f"\nAgent: {last_message.content}\n")
        # elif "__interrupt__" not in response:
        #     print(f"\nAgent completed the task.\n")

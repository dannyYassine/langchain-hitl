from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime
from langchain.chat_models import init_chat_model
from typing import Any, Optional


class ValidateWeatherQuestionGuardrail(AgentMiddleware):
    """Middleware to validate weather-related questions."""

    def __init__(self) -> None:
        super().__init__()
        self.safety_model = init_chat_model("gpt-5-mini")

    @hook_config(can_jump_to=["end"])
    def before_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        content = self._get_user_message_content(state)
        if content is None:
            return None

        safety_prompt = self._get_prompt(content)

        result = self.safety_model.invoke([{"role": "user", "content": safety_prompt}])

        if "ERROR" in result.content:
            # Block execution before any processing
            print(f"❌ Validation failed: {result.content}")
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": "I cannot process questions outside of weather-related questions in Canada and the United States. Please rephrase your question. Try again.",
                    }
                ],
                "structured_response": None,
                "jump_to": "end",
            }

        print("✅ Validation passed - proceeding with agent execution")

        return None

    def _get_user_message_content(self, state: AgentState) -> Optional[str]:
        """Extract and return the latest user message content.

        Args:
            state: Current agent state containing messages

        Returns:
            Lowercase user message content, or None if no valid user message found
        """
        if not state["messages"]:
            return None

        first_message = state["messages"][-1]
        if first_message.type != "human":
            return None

        message: str = first_message.content

        return message.lower()

    def _get_prompt(self, content: str) -> str:
        # Use a model to evaluate safety
        return f"""
        Evaluate if this question is only about weather-related questions in Canada and/or United States.
        Respond starting only with 'VALID' or 'ERROR', then a small sentence explaining the reason.

        Question: {content}"""

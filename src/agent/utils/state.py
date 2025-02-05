from .prompts import SYSTEM_PROMPT
from langgraph.graph import MessagesState
from langchain_core.messages import AnyMessage, SystemMessage


class AgentState(MessagesState):
    category: str


def initialize_state() -> AgentState:
    messages: list[AnyMessage] = [
        SystemMessage(content=SYSTEM_PROMPT),
    ]
    return {
        "messages": messages,
        "category": "",
    }


def update_state(state: AgentState, **kwargs) -> AgentState:
    for key, value in kwargs.items():
        if key in state:
            state[key] = value
    return state

from typing import Any, Dict

from langgraph.graph import MessagesState


class AgentState(MessagesState):
    summary: str
    similar_manual: Dict[str, Any]


def initialize_state() -> AgentState:
    return {"summary": "", "similar_manual": {}, "messages": []}


def update_state(state: AgentState, **kwargs) -> AgentState:
    for key, value in kwargs.items():
        if key in state:
            state[key] = value
    return state

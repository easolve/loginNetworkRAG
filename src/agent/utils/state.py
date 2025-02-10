from typing import Any, Dict

from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.graph import MessagesState

from agent.utils.constants import Mode
from agent.utils.prompts import SYSTEM_PROMPT


class AgentState(MessagesState):
    mode: Mode
    summary: str
    similar_manual: Dict[str, Any]
    known_info: Dict[str, Any]


def initialize_state() -> AgentState:
    messages: list[AnyMessage] = [
        SystemMessage(content=SYSTEM_PROMPT),
    ]
    return {
        "mode": Mode.KNOWLEDGE,
        "summary": "",
        "similar_manual": {},
        "known_info": {},
        "messages": messages,
    }


def update_state(state: AgentState, **kwargs) -> AgentState:
    for key, value in kwargs.items():
        if key in state:
            state[key] = value
    return state

from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    category: str
    is_end: bool


def initialize_state(messages: Sequence[BaseMessage] = []) -> AgentState:
    return {"messages": messages, "category": "", "is_end": False}

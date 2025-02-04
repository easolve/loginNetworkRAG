from langgraph.graph import MessagesState
from langchain_core.messages import AnyMessage


class AgentState(MessagesState):
    category: str
    is_end: bool


def initialize_state(messages: list[AnyMessage] = []) -> AgentState:
    return {"messages": messages, "category": "", "is_end": False}

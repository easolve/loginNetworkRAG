from langgraph.graph import MessagesState
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage


class AgentState(MessagesState):
    category: str
    is_end: bool


def initialize_state() -> AgentState:
    messages: list[AnyMessage] = [
        SystemMessage(content="당신은 AI CC 상담 챗봇입니다."),
    ]
    return {"messages": messages, "category": "", "is_end": False}

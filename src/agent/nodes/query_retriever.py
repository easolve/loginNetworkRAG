from src.agent.utils.prompts import SYSTEM_PROMPT
from src.agent.utils.state import AgentState
from src.agent.nodes.tool_node import manual_tool
from langchain_core.messages import SystemMessage, AIMessage


# manual tool을 사용해 질문에 대한 Retriever 반환 후 저장
def query_retriever(state: AgentState):
    messages = state["messages"]
    if len(state["messages"]) < 2:
        messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))

    # 질문과 가장 가까운 매뉴얼을 찾아서 반환
    similar_manual = manual_tool(state["messages"][-1].content)
    return {"similar_manual": similar_manual}


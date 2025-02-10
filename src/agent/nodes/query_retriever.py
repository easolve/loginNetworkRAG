from langchain_core.messages import SystemMessage

from agent.tools.manual_tool import manual_tool
from agent.utils.prompts import SYSTEM_PROMPT
from agent.utils.state import AgentState


# manual tool을 사용해 질문에 대한 Retriever 반환 후 저장
def query_retriever(state: AgentState):
    messages = state["messages"]
    if len(state["messages"]) < 2:
        messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))

    # 질문과 가장 가까운 매뉴얼을 찾아서 반환
    if isinstance(messages[-1].content, str):
        similar_manual = manual_tool(messages[-1].content)
        return {"similar_manual": similar_manual}

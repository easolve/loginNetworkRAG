from src.agent.utils.prompts import SYSTEM_PROMPT
from src.agent.utils.state import AgentState
from src.agent.nodes.tool_node import manual_tool
from langchain_core.messages import SystemMessage, AIMessage


def query_analysis(state: AgentState):
    messages = state["messages"]
    if len(state["messages"]) < 2:
        messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))

    res = manual_tool(state["messages"][-1].content)
    message_content = res["response"]
    return {"messages": AIMessage(content=message_content)}

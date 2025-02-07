from src.agent.utils.state import AgentState
from src.agent.utils.constants import MODEL
from src.agent.utils.prompts import AGENT_PROMPT
from src.agent.nodes.tool_node import tools
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import json


def cc_agent(state: AgentState):
    last_message = state["messages"][-1]
    messages = "".join([str(m.content) for m in state["messages"] if isinstance(m.content, str)])
    if isinstance(last_message, ToolMessage):
        content_dict = json.loads(last_message.content)
        user_info = content_dict.get("user_info", "")
        agent_info = content_dict.get("agent_info", "")
        model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
        chain = AGENT_PROMPT | model_with_tools
        res = chain.invoke({"messages": messages, "user_info": user_info, "agent_info": agent_info})
        return {"messages": [res], "user_info": user_info, "agent_info": agent_info}
    model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
    res = model_with_tools.invoke(state["messages"])
    return {"messages": [res]}


if __name__ == "__main__":
    print("This is a CC agent.")

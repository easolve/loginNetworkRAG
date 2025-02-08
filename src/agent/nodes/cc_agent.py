from src.agent.utils.state import AgentState
from src.agent.utils.constants import MODEL
from src.agent.utils.prompts import AGENT_PROMPT
from src.agent.nodes.tool_node import tools
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import json


def cc_agent(state: AgentState):
    messages = "".join([str(m.content) for m in state["messages"] if isinstance(m.content, str)])
    model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
    chain = AGENT_PROMPT | model_with_tools
    res = chain.invoke({"messages": messages, "similar_input": state["similar_manual"]["similar_input"], "manual": state["similar_manual"]["manual"]})
    return {"messages": [res]}


if __name__ == "__main__":
    print("This is a CC agent.")

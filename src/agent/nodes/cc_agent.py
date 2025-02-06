from src.agent.utils.state import AgentState
from src.agent.utils.constants import MODEL
from src.agent.nodes.tool_node import tools
from langchain_openai import ChatOpenAI


def cc_agent(state: AgentState):
    model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
    res = model_with_tools.invoke(state["messages"])
    return {"messages": [res]}


if __name__ == "__main__":
    print("This is a CC agent.")

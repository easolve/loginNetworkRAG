from src.agent.utils.state import AgentState
from src.agent.nodes.cc_agent import cc_agent
from src.agent.nodes.query_retriever import query_retriever
from src.agent.nodes.query_checker import query_checker
from src.agent.nodes.tool_node import tool_node
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver


def get_graph() -> CompiledStateGraph:
    builder = StateGraph(AgentState)
    builder.add_node("query_retriever", query_retriever)
    builder.add_node("query_checker", query_checker)
    builder.add_node("cc_agent", cc_agent)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "query_retriever")
    builder.add_conditional_edges("cc_agent", tools_condition, ["tools", END])
    builder.add_edge("tools", "cc_agent")
    builder.add_edge("query_retriever", "query_checker")
    builder.add_edge("query_checker", END)

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph


if __name__ == "__main__":
    get_graph()

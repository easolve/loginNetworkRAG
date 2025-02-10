from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition

from agent.nodes.cc_agent import cc_agent
from agent.nodes.query_retriever import query_retriever
from agent.nodes.tool_node import tool_node
from agent.utils.state import AgentState


def get_graph() -> CompiledStateGraph:
    builder = StateGraph(AgentState)
    builder.add_node("query_retriever", query_retriever)
    builder.add_node("cc_agent", cc_agent)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "query_retriever")
    builder.add_edge("query_retriever", "cc_agent")
    builder.add_conditional_edges("cc_agent", tools_condition, ["tools", END])
    builder.add_edge("tools", "cc_agent")

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph


if __name__ == "__main__":
    get_graph()

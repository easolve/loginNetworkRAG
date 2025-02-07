from src.agent.utils.state import AgentState
from src.agent.utils.constants import Category
from src.agent.nodes.cc_agent import cc_agent
from src.agent.nodes.query_analysis import query_analysis
from src.agent.nodes.tool_node import tool_node
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver


def get_graph() -> CompiledStateGraph:
    builder = StateGraph(AgentState)
    builder.add_node("query_analysis", query_analysis)
    builder.add_node("cc_agent", cc_agent)
    builder.add_node("tools", tool_node)

    def query_condition(state: AgentState):
        return END if state["category"] == Category.PENDING_JUDGMENT.value else "cc_agent"

    builder.add_edge(START, "query_analysis")
    builder.add_conditional_edges("query_analysis", query_condition, [END, "cc_agent"])
    builder.add_conditional_edges("cc_agent", tools_condition, ["tools", END])
    builder.add_edge("tools", "cc_agent")

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph


if __name__ == "__main__":
    get_graph()

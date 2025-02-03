from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from .utils.state import AgentState
from .utils.nodes import query_analysis, cc_agent
from .utils.tools import retriever_tool


def get_graph() -> CompiledStateGraph:
    retrieve = ToolNode([retriever_tool])

    builder = StateGraph(AgentState)
    builder.add_node("query_analysis", query_analysis)
    builder.add_node("cc_agent", cc_agent)
    builder.add_node("tools", retrieve)

    def query_condition(state: AgentState):
        return END if state["messages"] else "cc_agent"

    def agent_condition(state: AgentState):
        return "tools" if state["messages"] else END

    builder.add_edge(START, "query_analysis")
    builder.add_conditional_edges("query_analysis", query_condition, [END, "cc_agent"])
    builder.add_conditional_edges("cc_agent", agent_condition, ["tools", END])
    builder.add_edge("tools", "cc_agent")

    graph = builder.compile()
    return graph


if __name__ == "__main__":
    get_graph()

from .utils.state import AgentState
from .utils.nodes import query_analysis, cc_agent, tool_node
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import AIMessage


def get_graph() -> CompiledStateGraph:
    builder = StateGraph(AgentState)
    builder.add_node("query_analysis", query_analysis)
    builder.add_node("cc_agent", cc_agent)
    builder.add_node("tools", tool_node)

    def query_condition(state: AgentState):
        return END if state["is_end"] == True else "cc_agent"

    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        return (
            "tools"
            if isinstance(last_message, AIMessage) and last_message.tool_calls
            else END
        )

    builder.add_edge(START, "query_analysis")
    builder.add_conditional_edges("query_analysis", query_condition, [END, "cc_agent"])
    builder.add_conditional_edges("cc_agent", should_continue, ["tools", END])
    builder.add_edge("tools", "cc_agent")

    graph = builder.compile()
    return graph


if __name__ == "__main__":
    get_graph()

from src.agent.utils.state import AgentState
from src.agent.utils.constants import Category
from src.agent.nodes.cc_agent import cc_agent
from src.agent.nodes.query_analysis import query_analysis
from src.agent.nodes.tool_node import tool_node
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage


def get_graph() -> CompiledStateGraph:
    builder = StateGraph(AgentState)
    builder.add_node("query_analysis", query_analysis)
    builder.add_node("cc_agent", cc_agent)
    builder.add_node("tools", tool_node)

    def query_condition(state: AgentState):
        return END if state["category"] == Category.PENDING_JUDGMENT.value else "cc_agent"

    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        return "tools" if isinstance(last_message, AIMessage) and last_message.tool_calls else END

    builder.add_edge(START, "query_analysis")
    builder.add_conditional_edges("query_analysis", query_condition, [END, "cc_agent"])
    builder.add_conditional_edges("cc_agent", should_continue, ["tools", END])
    builder.add_edge("tools", "cc_agent")

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph


if __name__ == "__main__":
    get_graph()

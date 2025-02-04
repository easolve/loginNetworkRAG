from .state import AgentState
from .constants import MODEL
from .prompts import Category, QUERY_ANALYSIS_PROMPT
from .tools import retriever_tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field


def query_analysis(state: AgentState):
    class Analysis(BaseModel):
        category: Category = Field(description="판단 결과")

    query = state["messages"][-1].content
    model = ChatOpenAI(model=MODEL, temperature=0)

    model_with_tool = model.with_structured_output(Analysis)
    chain = QUERY_ANALYSIS_PROMPT | model_with_tool

    res = chain.invoke({"query": query})
    category: str = res.category.value
    new_is_end = True if category == Category.PENDING_JUDGMENT.value else False
    return {"is_end": new_is_end}


tools = [retriever_tool]
tool_node = ToolNode(tools)


def cc_agent(state: AgentState):
    model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
    if isinstance(state["messages"][-1], HumanMessage):
        return {
            "messages": [
                AIMessage(
                    content="",
                    tool_calls=[{
                        "name": "retriever_tool",
                        "args": {"question": state["messages"][-1].content},
                        "id": "tool_call_1",
                        "type": "tool_call",
                    }],
                )
            ]
        }
    res = model_with_tools.invoke(state["messages"])
    return {"messages": [res]}

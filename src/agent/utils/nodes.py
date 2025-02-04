from .state import AgentState
from .constants import MODEL
from .prompts import QUERY_ANALYSIS
from .tools import retriever_tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field


def query_analysis(state: AgentState):
    class analysis(BaseModel):
        category: str = Field(description="질문 카테고리")

    query = state["messages"][0].content
    model = ChatOpenAI(model=MODEL, temperature=0)

    model_with_tool = model.with_structured_output(analysis)
    chain = QUERY_ANALYSIS | model_with_tool

    res = chain.invoke({"query": query})
    category = res["category"]
    new_is_end = True if category == "판단 보류" else False
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
                    tool_calls=[
                        {
                            "name": "retriever_tool",
                            "args": {"question": state["messages"][-1].content},
                            "id": "tool_call_1",
                            "type": "tool_call",
                        }
                    ],
                )
            ]
        }
    res = model_with_tools.invoke(state["messages"])
    return {"messages": [res]}

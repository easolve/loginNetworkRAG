from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from .state import AgentState
from .constants import MODEL
from .prompts import QUERY_ANALYSIS


def query_analysis(state: AgentState):
    class analysis(BaseModel):
        category: str = Field(description="")

    query = state["messages"][0]
    llm = ChatOpenAI(model=MODEL, temperature=0)

    llm_with_tool = llm.with_structured_output(analysis)
    chain = QUERY_ANALYSIS | llm_with_tool

    res = chain.invoke({"query": query})
    category = res.category
    new_is_end = True if category == "판단 보류" else False
    return {"is_end": new_is_end}


def cc_agent(state: AgentState):
    return {"messages": ["test"]}

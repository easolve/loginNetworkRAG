from src.agent.utils.constants import Category, MODEL
from src.agent.utils.prompts import SYSTEM_PROMPT, QUERY_ANALYSIS_PROMPT
from src.agent.utils.state import AgentState
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


def query_analysis(state: AgentState):
    class Analysis(BaseModel):
        category: Category = Field(description="판단 결과")

    messages = state["messages"]
    if len(state["messages"]) < 2:
        messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))

    messages_str = "".join(
        message.content for message in messages if isinstance(message.content, str)
    )
    # query = state["messages"][-1].content
    query = messages_str
    model = ChatOpenAI(model=MODEL, temperature=0)

    model_with_tool = model.with_structured_output(Analysis)
    chain = QUERY_ANALYSIS_PROMPT | model_with_tool

    res = chain.invoke({"query": query})
    category: str = res.category.value
    return {"category": category}

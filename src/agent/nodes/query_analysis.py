from src.agent.utils.prompts import QUERY_ANALYSIS_PROMPT, SYSTEM_PROMPT
from src.agent.utils.state import AgentState
from src.agent.utils.constants import MODEL, Category
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field


def query_analysis(state: AgentState):
    messages = state["messages"]
    if len(state["messages"]) < 2:
        messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))

    class Analysis(BaseModel):
        category: Category = Field(description="판단 결과")

    messages_str = "".join(
        message.content for message in messages[-5:] if isinstance(message.content, str)
    )
    # query = state["messages"][-1].content
    query = messages_str
    model = ChatOpenAI(model=MODEL, temperature=0)

    model_with_tool = model.with_structured_output(Analysis)
    chain = QUERY_ANALYSIS_PROMPT | model_with_tool

    res = chain.invoke({"query": query})
    category: str = res.category.value
    return {"messages": messages, "category": category}

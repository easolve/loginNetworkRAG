from agent.utils.prompts import QUERY_GRADE_PROMPT
from agent.utils.state import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langgraph.types import Command
from langgraph.graph import END

from pydantic import BaseModel, Field


class GradeDocuments(BaseModel):
    """Score for relevance check on given documents.
    documents could be a retrieved docs or queries."""

    score: str = Field(description="queries are relevant on given documents. 'yes', 'hold' or 'no'")


# similar_manual.similar_input과 함께 질문을 OpenAI에 전달해 의미가 같은지 판단.
def query_checker(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    checker = QUERY_GRADE_PROMPT | structured_llm_grader

    # TODO: 이전의 문맥도 같이 보내서 의미가 같은지 판단할 수 있도록 해야 함.(요약 or 전문)
    query = state["messages"][-1].content
    similar_inputs = state["similar_manual"]["similar_input"]
    res = checker.invoke({"query": query, "similar_inputs": similar_inputs})
    print(f"query: {query}, similar: {similar_inputs} score: {res.score}")
    if res.score == "yes":
        return Command(goto="cc_agent")
    elif res.score == "hold":
        # TODO: 전문 상담사 호출 node 추가
        return Command(
            goto=END,
            update={"messages": AIMessage(content="전문 상담사를 호출하고 질의를 끝내겠습니다.")},
        )
    else:
        return Command(goto=END, update={"messages": AIMessage(content="검색 결과가 없습니다.")})

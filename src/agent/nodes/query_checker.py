from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langgraph.types import Command
from pydantic import BaseModel, Field

from agent.utils.constants import MODEL, Mode
from agent.utils.prompts import QUERY_GRADE_PROMPT
from agent.utils.state import AgentState


class GradeDocuments(BaseModel):
    """Score for relevance check on given documents.
    documents could be a retrieved docs or queries."""

    score: str = Field(description="queries are relevant on given documents. 'yes', 'hold' or 'no'")


# similar_manual.similar_input과 함께 질문을 OpenAI에 전달해 의미가 같은지 판단.
def query_checker(state: AgentState):
    llm = ChatOpenAI(model=MODEL, temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    checker = QUERY_GRADE_PROMPT | structured_llm_grader

    # TODO: 현재는 모든 메시지를 합쳐서 전달하고 있음. 이후에는 요약된 메시지만 전달하도록 수정 필요.
    query = state["messages"][-1].content
    similar_inputs = state["similar_manual"]["similar_input"]
    res = checker.invoke({"query": query, "similar_inputs": similar_inputs})
    print(f"query: {query}, similar: {similar_inputs} score: {res.score}")
    if res.score == "yes":
        return {"mode": Mode.KNOWLEDGE}
    elif res.score == "hold":
        # TODO: 전문 상담사 호출 node 추가
        return Command(
            goto=END,
            update={"messages": AIMessage(content="전문 상담사를 호출하고 질의를 끝내겠습니다.")},
        )
    else:
        return {"mode": Mode.TASK}

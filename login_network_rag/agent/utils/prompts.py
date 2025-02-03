from langchain_core.prompts import PromptTemplate


QUERY_ANALYSIS = PromptTemplate(
    input_variables=["query"],
    template="""
    당신은 AI CC 상담 챗봇입니다.
    사용자의 질문을 받고, 다음 기준에 따라 판단하십시오.

    질의 범주 판단: 질문이 다음 범주 중 어디에 속하는지 분류하십시오.
    - '개인정보', '세금', '화물 진행', '수하인 변경', '연락처 변경', '기타' 중 하나를 선택하십시오.
    - 만약 범주가 명확하지 않다면 '판단 보류'를 선택하십시오.

    사용자의 질문:{query}""",
)

from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT = """당신은 통관, 특송 회사의 고객센터 챗봇입니다."""


QUERY_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""사용자의 질문이 어떤 질의 범주에 속하는지 분류하십시오.
질문의 의도가 불명확한 경우, 판단 보류로 분류하십시오.

질의 범주:
- 개인정보 (개인정보 관련 문의)
- 세금 (관세, 부가세 등 세금 관련 문의)
- 출고 (화물 출고 관련 문의)
- 미결 (처리되지 않은 사항 관련 문의)
- 검사 (화물 검사 관련 문의)
- 원산지 (원산지 증명 관련 문의)
- 금지 (수출입 금지 품목 관련 문의)
- 이사화물 (이사화물 통관 관련 문의)
- 통관 (일반 통관 절차 관련 문의)
- 기타 (위 카테고리에 속하지 않는 업무에 관련한 문의)

사용자의 질문: {query}""",
)

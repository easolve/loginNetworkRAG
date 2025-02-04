from langchain_core.prompts import PromptTemplate
from enum import Enum


class Category(str, Enum):
    PERSONAL_INFORMATION = "개인정보"
    TAX = "세금"
    RELEASE = "출고"
    PENDING = "미결"
    INSPECTION = "검사"
    ORIGIN = "원산지"
    PROHIBITED = "금지"
    MOVING_GOODS = "이사화물"
    RELEASE_AGAIN = "출고"
    CUSTOMS_CLEARANCE = "통관"
    ETC = "기타"
    PENDING_JUDGMENT = "판단 보류"


QUERY_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""당신은 AI CC 상담 챗봇입니다.
사용자의 질문을 받고, 다음 기준에 따라 판단하십시오.

질의 범주 판단: 질문이 다음 범주 중 어디에 속하는지 분류하십시오.
- 개인정보 (개인정보 관련 문의)
- 세금 (관세, 부가세 등 세금 관련 문의)
- 출고 (화물 출고 관련 문의)
- 미결 (처리되지 않은 사항 관련 문의)
- 검사 (화물 검사 관련 문의)
- 원산지 (원산지 증명 관련 문의)
- 금지 (수출입 금지 품목 관련 문의)
- 이사화물 (이사화물 통관 관련 문의)
- 통관 (일반 통관 절차 관련 문의)
- 기타 (위 카테고리에 속하지 않는 문의)
- 판단 보류 (질문의 의도가 불명확한 경우)

위 카테고리 중 정확히 하나만 선택하여 분류하십시오.

사용자의 질문: {query}""",
)

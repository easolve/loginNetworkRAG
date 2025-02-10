from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

SYSTEM_PROMPT = """당신은 통관, 특송 회사의 고객센터 한국어 챗봇입니다.
반드시 메뉴얼을 기반으로 답변하여야 합니다.
최대한 정보 전달에 목적성을 두고 10년차 응대 경력직 직원이 답변하는 것처럼 친절하고 프로페셔널하게 답변해야 합니다.
당신의 답에 공란이 있다면 그 공란을 사용하여 답변을 하는 것이 아니라 도구를 사용하여 정보를 얻거나 사용자에게 질문하여 정보를 얻어야 합니다.
"""

QUERY_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""사용자의 질문이 어떤 질의 범주에 속하는지 분류하십시오.
질문의 의도가 불명확한 경우, 판단 보류로 분류하십시오.

질의 범주:
- 개인정보 (연락처, 배송지 변경 등 개인정보 관련 문의)
- 세금 (관세, 부가세 등 세금 관련 문의)
- 출고 (배송, 화물 출고 등 관련 문의)
- 미결 (처리되지 않은 사항 관련 문의)
- 검사 (세관 검사, 화물 검사 관련 문의)
- 원산지 (원산지 증명 관련 문의)
- 금지 (수출입 금지 품목과 그에 대한 의사 소견서 관련 문의)
- 이사화물 (이사화물 통관 관련 문의)
- 통관 (일반 통관 절차 관련 문의)
- 기타 (위 카테고리에 속하지 않는 업무에 관련한 문의)

사용자의 질문: {query}""",
)

QUERY_GRADE_PROMPT = PromptTemplate(
    input_variables=["query", "similar_inputs"],
    template="""당신은 사용자의 질문과 예제 질문이 얼마나 유사한지 평가하는 채점자입니다.
엄격한 테스트일 필요는 없습니다. 목표는 잘못된 검색 결과를 필터링하는 것입니다.
예제 질문에 사용자 질문과 관련된 키워드 또는 의미가 포함되어 있으면 관련성 있는 것으로 평가하십시오.
문서가 질문과 관련이 있는지 여부를 나타내기 위해 'yes' 또는 'hold', 'no'로 점수를 제공하십시오.
'yes'는 문서와 질문이 같거나 굉장히 비슷한 의미를 가지고 있음을 나타냅니다. 만약 사용자의 질문이 빈칸이거나 너무 짧아서 의미를 알 수 없다면 'no'로 평가하십시오.
'hold'는 문서와 질문이 관련이 있거나 아래와 같은 질의 범주를 가짐을 나타냅니다.
[개인정보, 세금, 출고, 미결, 검사, 원산지, 금지, 이사화물, 통관]
'no'는 의미도 같지 않으며 관련이 없음을 나타냅니다.
- '{query}'는 사용자의 질문입니다.
- '{similar_inputs}'는 사용자의 질문과 유사도를 비교할 예제 질문입니다.
""",
)

SUMMARIZE_PROMPT = PromptTemplate(
    input_variables=["conversation"],
    template="""지금까지의 대화 내용을 요약하십시오. 요약은 다음 대화를 이어가는데 필요한 중요한 정보만 포함해야 합니다.
요약에는 다음과 같은 내용이 포함되어야 합니다:
1. 사용자의 주요 문의 사항
2. 확인된 사용자 정보 (있는 경우)
3. 지금까지 제공된 주요 답변이나 안내 사항
4. 아직 해결되지 않은 사항 (있는 경우)

대화 내용:
{conversation}

요약본을 생성하십시오.""",
)

# QUESTION: ChatPromptTemplate vs PromptTemplate

EXTRACTION_EXPERT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with reference examples.
        ("human", "{text}"),
    ]
)

KNOWLEDGE_AGENT_PROMPT = PromptTemplate(
    input_variables=["messages", "manual", "info", "similar_input", "response"],
    template="""<instruction>
아래의 내용을 참고하고 tool을 사용해서, 'manual'대로 실행하십시오.
- 'conversation': 현재까지의 대화 내용
- 'similar_input': 사용자의 질문과 같거나 유사한 의도를 가진 질문
- 'response': 'similar_input'에 대한 답변
- 'info': 사용자의 질문에 대한 추가 정보
- 'manual': 사용자의 질문에 대한 답변을 참고할 수 있는 메뉴얼
'manual'대로 실행이 끝났다면 tool을 사용하지 말고 사용자에게 결과를 알려주십시오.
만약 정보가 부족하다면 tool을 사용하지 말고 사용자에게 'info'를 요구하십시오.
**대화에서 같은 내용이 반복된다면, tool을 더 이상 호출하지 않고 결과를 사용자에게 알려주십시오.**
</instruction>

<task_description>
## similar_input:
{similar_input}
## response:
{response}
## manual:
{manual}
## info:
{info}
</task_description>

<conversation>
{messages}
</conversation>""",
)

TASK_AGENT_PROMPT = PromptTemplate(
    input_variables=["messages"],
    template="""
다음은 사용자와의 대화 내용입니다:
{messages}""",
)

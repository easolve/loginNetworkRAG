import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.agent.agent import get_graph


@pytest.fixture(name="test_graph")
def graph():
    """테스트에서 사용할 그래프 객체를 생성합니다."""
    return get_graph()


def test_graph_basic_flow(test_graph):
    """기본적인 그래프 실행 흐름을 테스트합니다."""
    # 테스트용 입력 메시지
    test_message = "통관 절차에 대해 알려주세요"

    # 입력 준비
    input_data = {"messages": [HumanMessage(content=test_message)]}
    config = {"configurable": {"thread_id": "test-1"}}

    # 그래프 실행
    result = test_graph.invoke(input_data, config)

    # 결과 검증
    assert "messages" in result
    assert isinstance(result["messages"][-1], AIMessage)
    assert len(result["messages"]) > 0


def test_error_handling(test_graph):
    """에러 처리를 테스트합니다."""
    # 잘못된 입력으로 테스트
    with pytest.raises(Exception):
        test_graph.invoke({"messages": []})


def test_predefined_questions(test_graph):
    """미리 정의된 질문들에 대한 응답을 테스트합니다."""
    test_cases = [
        "개인정보 오류 관련해서 알림톡 받았는데 확인해주세요",
        "수하인 변경 문의 ex) 이름을 변경하고 싶어요.",
        "화물 진행 정보 문의 ex) 물품이 국내에 도착했다고 하는데 진행 상황을 알고 싶어요.",
        "연락처 변경 요청 ex) 연락처를 변경하고 싶어요.",
        "통관번호 오류인데 보내주신 카톡으로 수정이 불가능해요",
        "세금 납부했는데 주문 물건 언제쯤 받아볼 수 있을까요?",
        "계좌 입금 확인 요청 ex) 납부한 세액이 입금되었는지 확인하고 싶어요.",
        "세액 안내 요청 (문자 발송) ex) 세액 문자가 오지 않아요. 문자를 다시 보내주세요.",
        "세액 안내 연락처 변경 요청 ex) 세액 안내를 다른 연락처로 받고 싶어요.",
        "세금확인요청 ex)예상 세액과 청구받은 세액이 달라요. 어떻게 계산된 건지 알고 싶어요.",
        "자금청구서 및 필증,계산서,영수증 요청  ex) 통관 관련한 서류를 받고 싶어요.",
        "가격 및 품명 정정 요청 문의 ex) 실제 구매한 가격과 신고된 가격이 달라요.",
        "FTA 협정 적용 요청 문의 (원산지 증명서 등) ex) 원산지증명서를 내라는 문자를 받았어요.",
        "관부가세문의 ex)관부가세가 무엇이며 왜 세금이 발생했는지 궁금해요.",
        "골동품세금 ex)골동품인데 왜 세금이 발생했는지 궁금해요.",
        "주류세금 ex)기타세가 뭔가요?",
        "주류관련 ex)술이 아니라 빈병인데 세금이 너무 많이나왔어요.",
        "합산 과세 안내 요청 ex) 제 물건이 합산되었다는 문자를 받았어요. 설명을 듣고 싶어요.",
        "건기식 및 의약품 관련 수량초과건 문의 ex) 수량초과가 되어 통관이 지연되고 있다는 문자를 받았어요. 어떤 서류가 필요한가요?",
        "통관 보류 물품 현황 안내 (통관불가 물품, 금지성분 등) ex) 제 물품이 세관에서 통관보류 되었다는 안내를 받았어요.",
        "가격자료 제출관련 ex)가격자료 관련하여 문자를 받았어요.",
        "중고 물품 입증자료",
        "상용의심 관련 문의 ex) 상용의심관련 문자를 받았어요. 설명을 듣고 싶어요.",
        "국내에서 판매하고있는 제품인데 왜 금지성분인가요?",
        "그전에는 통관됬던 제품인데 왜 금지성분으로 걸린거죠?",
        "의사소견서 제출기한이 어떻게 되나요?",
        "소견서 제출했는데 언제 통관되나요?",
        "소견서 어떤식으로 작성해야하나요? / 어디로 보내야하나요?",
        "세관 검사 문의 ex) 검사는 왜 걸린건가요?",
        "세관 검사 시점 ex) 세관 검사는 언제 되나요?",
        "세관검사 처리 ex) 세관 검사 처리는 언제 끝나나요?",
        "원산지 미국(또는 중국)인데 왜 협정적용이 안되어있죠?",
        "세금납부하고 물품이 도착했는데 주문한 물품과 다른 물품을 받았어요",
        "건강기능식품, 의약품 수량초과 / 저는 6개 구입했는데 수량초과로 안내받았어요",
        "배송지 변경 및 배송 문의 ex) 배송지를 변경하고 싶어요.",
        "택배사 문의 및 출고 예상일 문의 (반출/배송 등) ex) 물품이 언제 도착하는지 궁금해요.",
        "방물출고 가능한가요?",
        "퀵 배송 가능한가요?",
        "주소지변경요청",
        "직접 물건을 찾으러 오고 싶어요",
        "사업자 통관의 경우 어떻게 처리되나요?",
        "아직 입국전이라 출입국증명서 발급이 안되는데요",
        "가족이 대신 받아주는 화물이라서 입국자와 성명이 달라요",
        "나이가 있어서 AI 못해요 담당자 연결해주세요",
    ]

    with open("res.md", "w", encoding="utf-8") as f:
        for question in test_cases:
            input_data = {"messages": [HumanMessage(content=question)]}
            config = {"configurable": {"thread_id": f"test-{question[:10]}"}}

            result = test_graph.invoke(input_data, config)

            # 응답 검증
            assert "messages" in result
            assert isinstance(result["messages"][-1], AIMessage)
            response_content = result["messages"][-1].content
            assert len(response_content) > 0

            # 질문과 응답을 markdown 파일에 기록
            f.write(f"## 질문: {question}\n")
            f.write(f"## 응답: {response_content}\n\n")

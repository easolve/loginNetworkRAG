from langchain.tools import tool
from typing import Dict



@tool
def get_customs_info_tool() -> Dict:
    """
    유니패스(UNIPASS)를 통해 통관 정보를 제공합니다.
    알 수 있는 통관 정보는 다음과 같습니다.
    - 사용자 구매금액, 사용자 신고 금액, 화물의 현재 진행 상태

    - purchase_amount: 사용자 구매금액
    - declared_amount: 사용자 신고 금액
    - current_status: 화물의 현재 진행 상태
    Returns:
        Dict: {
            "purchase_amount": float,
            "declared_amount": float,
            "current_status": str,
        }
    """
    print("--- get_customsers_info_tools ---")
    return {
        "purchase_amount": 100.0,
        "declared_amount": 100.0,
        "current_status": "배송 중",
    }

from langchain.tools import tool
from typing import Dict

@tool
def get_deposit_details_tool() -> Dict:
    """
    계좌의 입금내역을 조회하고 결과를 반환합니다.

    - success: 메시지 전송 성공 여부
    Returns:
        Dict: {
            "success": bool,
        } 
    """
    print("--- get_deposit_details_tool ---")
    return {"success": True}
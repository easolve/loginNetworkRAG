from typing import Dict

from langchain.tools import tool

from agent.utils.constants import CARRIER_INFO, ExpressCourier


@tool
def express_carrier_tool(name: ExpressCourier) -> Dict:
    """
    사용자가 특송 업체에 직접 문의할 수 있도록 특송사의 정보를 제공합니다.
    이메일과 전화번호를 제공합니다.

    Returns:
        Dict: {
            "email": str,
            "Telephone": str,
        }
    """
    print("--- express_carrier_tool ---")
    return CARRIER_INFO.get(name, {"email": "정보 없음", "Telephone": "정보 없음"})

from typing import Dict

from langchain.tools import tool

from agent.utils.constants import CARRIER_INFO, ExpressCourier


@tool
def express_carrier_tool(name: ExpressCourier) -> Dict:
    """
    특송사, 관세사, 고객센터(회사) 중 특송사의 이메일과 전화번호를 제공합니다.
    특송사에 직접 문의할 수 있도록 특송사의 정보를 활용할 수 있습니다.
    고객센터의 정보는 `company_info_tool`을 사용하세요.

    Returns:
        Dict: {
            "email": str,
            "Telephone": str,
        }
    """
    print("--- express_carrier_tool ---")
    return CARRIER_INFO.get(name, {"email": "정보 없음", "Telephone": "정보 없음"})

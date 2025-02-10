from typing import Dict

from langchain.tools import tool


@tool
def customs_broker_tool() -> Dict:
    """
    관세 정보를 제공합니다.

    Returns:
      Dict: {
        "response": str,
        "customs_data": Dict
      }
    """
    fake_customs_data = {
        "item": "전자제품",
        "value": "1000 USD",
        "duty": "5%",
        "tax": "10%",
        "total_cost": "1150 USD",
    }

    return {"response": "통관 정보를 제공합니다.", "customs_data": fake_customs_data}

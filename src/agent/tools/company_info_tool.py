from typing import Dict

from langchain.tools import tool


@tool
def company_info_tool() -> Dict:
    """
    특송사, 관세사, 고객센터(회사) 중 고객센터의 이메일과 담당자 전화번호를 제공합니다.
    사용자가 제출해야 하는 문서, 서류가 있을 경우에 이 정보를 활용할 수 있습니다.
    특송사의 정보는 `express_carrier_tool`을 사용하세요.

    Returns:
      Dict: {
        "email": str,
        "Telephone": str,
      }
    """
    print("--- company_info_tool ---")
    return {"email": "express@wscustoms.co.kr", "Telephone": "02-1234-5678"}

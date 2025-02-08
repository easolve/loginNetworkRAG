from langchain.tools import tool
from typing import Dict


@tool
def company_info_tool() -> Dict:
    """
    회사의 정보를 제공합니다.
    사용자가 필요한 문서나 정보를 얻을 수 있도록 이메일과 담당자 전화번호를 제공합니다.

    Returns:
        Dict: {
            "email": str,
            "Telephone": str,
        }
    """
    print("--- company_info_tool ---")
    return {"email": "express@wscustoms.co.kr", "Telephone": "02-1234-5678"}

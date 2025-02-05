from langchain.tools import tool
from typing import Dict


@tool
def customs_carrier_tool() -> Dict:
    """
    통관 정보를 제공합니다.

    Returns:
        Dict: {
            "category": str,
            "input": str,
            "response": str
        }
    """
    return {
        "category": "통관",
        "input": "통관 정보",
        "response": "통관 정보를 제공합니다.",
    }

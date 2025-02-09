from typing import Dict

from langchain.tools import tool


@tool
def customs_broker_tool() -> Dict:
    """
    관세 정보를 제공합니다.

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

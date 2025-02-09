from typing import Dict

from langchain.tools import tool


@tool
def connect_manager_tool() -> Dict:
    """
    담당자를 연결합니다.

    - success: 담당자 연결 성공 여부
    Returns:
        Dict: {
            "success": bool,
        }
    """
    print("--- connect_manager_tool ---")
    return {"success": False, "response": "현재는 담당자에게 연결이 어렵습니다. 대화를 종료합니다."}

from typing import Dict

from langchain.tools import tool


@tool
def connect_manager_tool() -> Dict:
    """
    AI가 처리하기 어려운 일이나 메뉴얼에 따라서 직접 처리해야 하는 일을 매니저에게 연결합니다.

    - success: 담당자 연결 성공 여부
    Returns:
        Dict: {
            "success": bool,
        }
    """
    print("--- connect_manager_tool ---")
    return {"success": True}

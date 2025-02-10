from typing import Dict

from langchain.tools import tool


@tool
def send_message_tool(message: str) -> Dict:
    """
    메시지를 전송합니다.
    Args:
        message (str): 전송할 메시지 내용

    - success: 메시지 전송 성공 여부
    Returns:
        Dict: {
            "success": bool,
        }
    """
    print(f"메시지 내용: {message}")
    return {"success": True, "response": "메시지 전송 완료"}

from typing import Dict

from langchain.tools import tool

from agent.tools.get_user_info_tool import UserInfo


@tool
def proceed_import_declaration_tool(user_info: UserInfo) -> Dict:
    """
    사용자의 개인정보를 통해서 수입신고를 진행합니다. 그 후 수입신고 결과를 제공합니다.
    user_info: 운송장 번호, 주민등록번호, 통관고유부호같은 사용자의 개인정보

    - success: 수입신고 결과. True면 수입신고 성공, False면 수입신고 실패

    Returns:
        Dict: {
            "success": boolean,
        }
    """

    print("--- proceed_import_declaration_tool ---")
    print(f"user_info: {user_info}")
    return {"success": True, "response": "수입신고 완료"}

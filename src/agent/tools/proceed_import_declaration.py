from src.agent.tools.get_user_info import UserInfo
from typing import Dict

from langchain.tools import tool

@tool
def proceed_import_declaration(user_info: UserInfo) -> Dict:
    """
    사용자의 개인정보를 통해서 수입신고를 진행합니다. 그 후 수입신고 결과를 제공합니다.
    user_info: 운송장 번호, 주민등록번호, 통관고유부호같은 사용자의 개인정보

    - result: 수입신고 결과
    
    Returns:
        Dict: {
            "result": boolean,
        }
    """

    user_info
    return {"result": True}
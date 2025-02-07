from langchain.tools import tool
from typing import Dict, Optional


class UserInfoStorage:
    def __init__(self):
        self.storage = {}

    def save_user_info(self, name: str, address: str, waybill_number: str) -> None:
        self.storage[name] = {
            "name": name,
            "address": address,
            "waybill_number": waybill_number,
        }

    def get_user_info(self, name: str) -> Optional[Dict]:
        return self.storage.get(name)


storage = UserInfoStorage()


@tool
def save_user_info_tool(name: str, address: str, waybill_number: str) -> Dict:
    """
    현재 대화하고 있는 사용자의 정보를 저장합니다.

    Args:
        name (str): 사용자 이름
        address (str): 사용자 주소
        waybill_number (str): 사용자 운송장 번호

    Returns:
        Dict: {
            "status": str,
            "message": str
        }
    """
    try:
        storage.save_user_info(name, address, waybill_number)
        return {"status": "success", "message": f"{name}님의 정보가 저장되었습니다."}
    except Exception as e:
        return {"status": "error", "message": f"정보 저장 중 오류 발생: {str(e)}"}


@tool
def get_user_info_tool(name: str) -> Dict:
    """
    사용자의 개인 정보가 필요할 때 사용자 이름을 입력받아 사용자 정보를 조회합니다.

    Args:
        name (str): 조회할 사용자 이름

    Returns:
        Dict: {
            "status": str,
            "user_info": Optional[Dict]
        }
    """
    try:
        user_info = storage.get_user_info(name)
        if user_info:
            return {"status": "success", "user_info": user_info}
        return {
            "status": "not_found",
            "message": f"{name}님의 정보를 찾을 수 없습니다.",
        }
    except Exception as e:
        return {"status": "error", "message": f"정보 조회 중 오류 발생: {str(e)}"}

from langchain.tools import tool
from typing import Dict
from enum import Enum


class ExpressCourier(Enum):
    PATECH = "파테크"
    SGL = "SGL"
    NAMGYEONG = "남경"
    LOGISTORM = "로지스톰"
    LOTOS = "LOTOS"
    ACE = "ACE"


CARRIER_INFO = {
    ExpressCourier.PATECH: {
        "email": "admin@forwarder.kr",
        "Telephone": "032-201-1155",
    },
    ExpressCourier.SGL: {
        "email": "sgl@siriusglobal.co.kr",
        "Telephone": "051-441-7341",
    },
    ExpressCourier.NAMGYEONG: {
        "email": "gtjeon@namkyungglobal.com",
        "Telephone": "02-577-3331",
    },
    ExpressCourier.LOGISTORM: {
        "email": "logistormail@gmail.com",
        "Telephone": "02-2667-0306",
    },
    ExpressCourier.LOTOS: {
        "email": "sale@lotos.co.jp",
        "Telephone": "+81-3-6278-9408",
    },
    ExpressCourier.ACE: {
        "email": "import2@iecoz.com",
        "Telephone": "02-2038-7224",
    },
}


@tool
def express_carrier_tool(name: ExpressCourier) -> Dict:
    """
    특송사의 정보를 제공합니다.
    사용자가 특송 업체에 직접 문의할 수 있는 이메일과 전화번호를 제공합니다.

    Returns:
        Dict: {
            "email": str,
            "Telephone": str,
        }
    """
    return CARRIER_INFO.get(name, {"email": "정보 없음", "Telephone": "정보 없음"})

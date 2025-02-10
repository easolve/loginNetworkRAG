import os
from enum import Enum
from getpass import getpass

from dotenv import load_dotenv

load_dotenv()


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass(f"Please enter your {var}: ")


_set_env("OPENAI_API_KEY")
_set_env("MODEL")


MODEL = os.environ["MODEL"]
CSV_PATH = "./data/manual.csv"
PERSIST_DIRECTORY = "./chroma_db"


class Category(str, Enum):
    PERSONAL_INFORMATION = "개인정보"
    TAX = "세금"
    RELEASE = "출고"
    PENDING = "미결"
    INSPECTION = "검사"
    ORIGIN = "원산지"
    PROHIBITED = "금지"
    MOVING_GOODS = "이사화물"
    RELEASE_AGAIN = "출고"
    CUSTOMS_CLEARANCE = "통관"
    ETC = "기타"
    PENDING_JUDGMENT = "판단 보류"


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


class Mode(str, Enum):
    TASK = "task"
    KNOWLEDGE = "knowledge"

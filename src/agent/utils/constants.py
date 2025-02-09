from getpass import getpass
from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass(f"Please enter your {var}: ")


_set_env("OPENAI_API_KEY")
_set_env("MODEL")


MODEL = os.environ["MODEL"]
CSV_PATH = "./data/manual.csv"


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

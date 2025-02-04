from getpass import getpass
from dotenv import load_dotenv
import os

load_dotenv()


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass(f"Please enter your {var}: ")


_set_env("OPENAI_API_KEY")
_set_env("MODEL")


MODEL = os.environ["MODEL"]
CSV_PATH = "./data/aIcs-ace.csv"

from typing import Optional
from pydantic import BaseModel, Field

from src.agent.utils.constants import MODEL 
from src.agent.utils.prompts import EXTRACTION_EXPERT

from langchain.tools import tool
from langchain_openai import ChatOpenAI


# https://python.langchain.com/docs/tutorials/extraction/
class UserInfo(BaseModel):
    """User information"""

    tracking_num: Optional[str] = Field(description="사용자가 시킨 물건의 운송장번호.")
    rrn: Optional[str] = Field(description="사용자의 주민등록번호.")
    custom_num: Optional[str] = Field(description="사용자의 통관고유부호(통관번호).")
    phone_num: Optional[str] = Field(description="사용자의 전화번호.")
    email: Optional[str] = Field(description="사용자의 이메일 주소.")

@tool
def get_user_info_tool(query: str) -> UserInfo:
    """
    사용자가 입력한 메시지를 분석하여 사용자의 개인정보인 주민등록번호, 운송장 번호, 통관번호, 전화번호, 이메일을 추출합니다.
    만약 특정 정보가 입력한 메시지에 없다면 해당 필드는 None을 반환합니다.
    """
    prompt = EXTRACTION_EXPERT.invoke({"text": query})
    structured_llm = ChatOpenAI(model=MODEL, temperature=0).with_structured_output(schema=UserInfo)
    res = structured_llm.invoke(prompt)
    print("--- get_user_info_tool ---")
    return res
    

    
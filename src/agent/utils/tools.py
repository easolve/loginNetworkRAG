from .logger import logger
from .constants import CSV_PATH
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.tools import tool
import pandas as pd
from typing import List, Dict


class RAGRetriever:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.embeddings = OpenAIEmbeddings()
        self.retriever = None

    def load_documents(self) -> List[Document]:
        try:
            df = pd.read_csv(self.csv_path)
            df = df.dropna(subset=["category", "input", "response"])
            return [
                Document(
                    page_content=row["input"],
                    metadata={"category": row["category"], "response": row["response"]},
                )
                for _, row in df.iterrows()
            ]
        except Exception as e:
            logger.error(f"문서 로딩 중 에러 발생: {e}")
            raise

    def setup_retriever(self, docs: List[Document]) -> None:
        try:
            vectorstore = Chroma.from_documents(
                documents=docs,
                collection_name="rag-chroma",
                embedding=self.embeddings,
            )
            self.retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
        except Exception as e:
            logger.error(f"리트리버 설정 중 에러 발생: {e}")
            raise

    def query(self, question: str) -> Dict:
        try:
            if not self.retriever:
                raise ValueError("Retriever가 초기화되지 않았습니다.")

            docs = self.retriever.get_relevant_documents(question)
            if not docs:
                return {
                    "category": "없음",
                    "input": question,
                    "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
                }

            doc = docs[0]
            return {
                "category": doc.metadata.get("category", "분류 정보 없음"),
                "input": doc.page_content,
                "response": doc.metadata.get("response", "응답 정보 없음"),
            }
        except Exception as e:
            logger.error(f"쿼리 실행 중 에러 발생: {e}")
            raise


retriever = RAGRetriever(CSV_PATH)
docs = retriever.load_documents()
retriever.setup_retriever(docs)


@tool
def retriever_tool(question: str) -> Dict:
    """
    질문에 대한 관련 정보를 검색하여 응답합니다.

    Args:
        question (str): 사용자의 질문

    Returns:
        Dict: {
            "category": str,
            "input": str,
            "response": str
        }
    """
    return retriever.query(question)


@tool
def customs_carrier_tool() -> Dict:
    """
    통관 정보를 제공합니다.

    Returns:
        Dict: {
            "category": str,
            "input": str,
            "response": str
        }
    """
    return {
        "category": "통관",
        "input": "통관 정보",
        "response": "통관 정보를 제공합니다.",
    }


from enum import Enum


class ExpressCourier(Enum):
    PATECH = "파테크"
    SGL = "SGL"
    NAMGYEONG = "남경"
    LOGISTORM = "로지스톰"
    LOTOS = "LOTOS"
    ACE = "ACE"


@tool
def express_carrier_tool(name: ExpressCourier) -> Dict:
    """
    특송사 정보를 제공합니다.

    Returns:
        Dict: {
            "email": str,
            "Telephone": str,
        }
    """
    match name:
        case ExpressCourier.PATECH:
            return {
                "email": "admin@forwarder.kr",
                "Telephone": "032-201-1155",
            }
        case ExpressCourier.SGL:
            return {
                "email": "sgl@siriusglobal.co.kr",
                "Telephone": "051-441-7341",
            }
        case ExpressCourier.NAMGYEONG:
            return {
                "email": "gtjeon@namkyungglobal.com",
                "Telephone": "02-577-3331",
            }
        case ExpressCourier.LOGISTORM:
            return {
                "email": "logistormail@gmail.com",
                "Telephone": "02-2667-0306",
            }
        case ExpressCourier.LOTOS:
            return {
                "email": "sale@lotos.co.jp ",
                "Telephone": "+81-3-6278-9408",
            }
        case ExpressCourier.ACE:
            return {
                "email": "import2@iecoz.com",
                "Telephone": "02-2038-7224",
            }
        case _:
            return {
                "email": "정보 없음",
                "Telephone": "정보 없음",
            }

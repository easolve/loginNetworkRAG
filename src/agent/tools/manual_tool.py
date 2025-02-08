from src.agent.utils.logger import logger
from src.agent.utils.constants import CSV_PATH
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.tools import tool
import pandas as pd
from typing import List, Dict


class RAGRetriever:
    def __init__(self, path: str):
        self.path = path
        self.embeddings = OpenAIEmbeddings()
        self.retriever = None

    def load_documents(self) -> List[Document]:
        try:
            df = pd.read_csv(self.path)
            df = df.dropna(
                subset=[
                    "category",
                    "request",
                    "response",
                ]
            )
            return [
                Document(
                    page_content=row["request"],
                    metadata={
                        "category": row["category"],
                        "manual": row["manual"],
                        "info" : row["info"],
                        "response": row["response"],
                    },
                )
                for _, row in df.iterrows()
            ]
        except Exception as e:
            logger.error("문서 로딩 중 에러 발생: %s", e)
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
            logger.error("리트리버 설정 중 에러 발생: %s", e)
            raise

    def query(self, question: str) -> Dict:
        try:
            if not self.retriever:
                raise ValueError("Retriever가 초기화되지 않았습니다.")

            docs = self.retriever.invoke(question)
            if not docs:
                return {
                    "category": "",
                    "manual": "",
                    "info": "",
                    "similar_input": "",
                    "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
                }

            doc = docs[0]
            return {
                "category": doc.metadata.get("category", ""),
                "similar_input": doc.page_content,
                "manual": doc.metadata.get("manual", ""),
                "info": doc.metadata.get("info", ""),
                "response": doc.metadata.get("response", ""),
            }
        except Exception as e:
            logger.error("쿼리 실행 중 에러 발생: %s", e)
            raise


retriever = RAGRetriever(CSV_PATH)
documents = retriever.load_documents()
retriever.setup_retriever(documents)


# TODO: retriever에서 request 부분만 user_input과 코사인 유사도 판별
@tool
def manual_tool(user_input: str) -> Dict:
    """
    모든 사용자의 입력에 대해 메뉴얼에서 가장 관련성 높은 답변을 찾아 반환합니다.

    Args:
        user_input (str): 사용자의 입력

    Returns:
        Dict: {
            "category": str,
            "manual": str,
            "info": str,
            "similar_input": str,
            "response": str,
        }
    """
    return retriever.query(user_input)

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
            df = df.dropna(subset=["분류", "input", "response"])
            return [
                Document(
                    page_content=row["input"],
                    metadata={"분류": row["분류"], "response": row["response"]},
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
                    "분류": "없음",
                    "input": question,
                    "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
                }

            doc = docs[0]
            return {
                "분류": doc.metadata.get("분류", "분류 정보 없음"),
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
            "분류": str,
            "input": str,
            "response": str
        }
    """
    return retriever.query(question)

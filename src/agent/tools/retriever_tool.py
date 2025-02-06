from src.agent.utils.logger import logger
from src.agent.utils.constants import CSV_PATH
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
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

            docs = self.retriever.get_relevant_documents(question)
            if not docs:
                return {
                    "category": "없음",
                    "similar_input": question,
                    "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
                }

            doc = docs[0]
            return {
                "category": doc.metadata.get("category", "없음"),
                "similar_input": doc.page_content,
                "response": doc.metadata.get("response", "없음"),
            }
        except Exception as e:
            logger.error("쿼리 실행 중 에러 발생: %s", e)
            raise


retriever = RAGRetriever(CSV_PATH)
documents = retriever.load_documents()
retriever.setup_retriever(documents)


@tool
def retriever_tool(user_input: str) -> Dict:
    """
    사용자의 입력에 대해서 가장 유사한 Q/A 문서를 제공합니다.
    사용자의 입력과 가장 유사한 응답이 같은 맥락이라면 해당 응답을 사용합니다.

    Args:
        user_input (str): 사용자의 입력

    Returns:
        Dict: {
            "category": str,
            "similar_input": str,
            "response": str
        }
    """
    return retriever.query(user_input)

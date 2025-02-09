from agent.utils.logger import logger
from agent.utils.constants import CSV_PATH
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
                        "user_info": row["user_info"],
                        "agent_info": row["agent_info"],
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
                    "user_info": "",
                    "agent_info": "",
                    "similar_input": "",
                    "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
                }

            doc = docs[0]
            return {
                "category": doc.metadata.get("category", ""),
                "user_info": doc.metadata.get("user_info", ""),
                "agent_info": doc.metadata.get("agent_info", ""),
                "similar_input": doc.page_content,
                "response": doc.metadata.get("response", ""),
            }
        except Exception as e:
            logger.error("쿼리 실행 중 에러 발생: %s", e)
            raise


retriever = RAGRetriever(CSV_PATH)
documents = retriever.load_documents()
retriever.setup_retriever(documents)


@tool
def manual_tool(user_input: str) -> Dict:
    """
    모든 사용자의 입력을 응대 메뉴얼에서 가장 관련성 높은 답변을 찾아 반환합니다.
    질문의 내용이 확실하지 않다면 메뉴얼을 참고하여 질문을 재정의합니다.

    Args:
        user_input (str): 사용자의 입력

    Returns:
        Dict: {
            "category": str,
            "user_info": str,
            "agent_info": str,
            "similar_input": str,
            "response": str,
        }
    """
    return retriever.query(user_input)

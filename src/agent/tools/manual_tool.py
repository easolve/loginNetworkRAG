import os
from typing import Any, Dict, List

import pandas as pd
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from agent.utils.constants import CSV_PATH, PERSIST_DIRECTORY
from agent.utils.logger import logger


class RAGRetriever:
    def __init__(self, path: str):
        self.path = path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

    def load_documents(self) -> List[Document]:
        try:
            df = pd.read_csv(self.path)
            df = df.dropna(subset=["category", "request", "response"])
            return [
                Document(
                    page_content=row["request"],
                    metadata={
                        "category": row["category"],
                        "manual": row["manual"],
                        "info": row["info"],
                        "response": row["response"],
                    },
                )
                for _, row in df.iterrows()
            ]
        except Exception as e:
            logger.error("문서 로딩 중 에러 발생: %s", e)
            raise

    def setup_retriever(self, docs: List[Document]) -> None:
        """
        persist directory에 저장된 벡터스토어가 있다면 재사용하고,
        없을 경우 새로 생성하여 저장합니다.
        """
        try:
            if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
                self.vectorstore = Chroma(
                    persist_directory=PERSIST_DIRECTORY,
                    embedding_function=self.embeddings,
                    collection_name="rag-chroma",
                )
                logger.info("기존 벡터스토어 로드 완료: %s", PERSIST_DIRECTORY)
            else:
                self.vectorstore = Chroma.from_documents(
                    documents=docs,
                    collection_name="rag-chroma",
                    embedding=self.embeddings,
                    persist_directory=PERSIST_DIRECTORY,
                )
                logger.info("벡터스토어 생성 완료: %s", PERSIST_DIRECTORY)
        except Exception as e:
            logger.error("ChromaDB 설정 중 에러 발생: %s", e)
            raise

    def query(self, question: str) -> Dict:
        try:
            if not self.vectorstore:
                raise ValueError("ChromaDB가 설정되지 않았습니다.")

            docs_with_scores = self.vectorstore.similarity_search_with_score(query=question, k=1)
            if not docs_with_scores:
                return {
                    "category": "",
                    "manual": "",
                    "info": "",
                    "similar_input": "",
                    "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
                    "score": 0,
                }

            # score는 코사인 거리이므로 1에서 빼줘야 유사도가 높은 문서일수록 점수가 높아짐
            doc, score = docs_with_scores[0]
            return {
                "category": doc.metadata.get("category", ""),
                "similar_input": doc.page_content,
                "manual": doc.metadata.get("manual", ""),
                "info": doc.metadata.get("info", ""),
                "response": doc.metadata.get("response", ""),
                "score": round(1 - score, 4),
            }
        except Exception as e:
            logger.error("쿼리 실행 중 에러 발생: %s", e)
            raise


retriever = RAGRetriever(CSV_PATH)
documents = retriever.load_documents()
retriever.setup_retriever(documents)


def manual_tool(user_input: str) -> Dict[str, Any]:
    """
    모든 사용자의 입력을 응대 메뉴얼에서 가장 관련성 높은 답변을 찾아 반환합니다.
    질문의 내용이 확실하지 않다면 메뉴얼을 참고하여 질문을 재정의합니다.

    Args:
        user_input (str): 사용자의 입력

    Returns:
        Dict: {
            "category": str,
            "manual": str,
            "info": str,
            "similar_input": str,
            "response": str,
            "score": float,
        }
    """
    res = retriever.query(user_input)
    if res["score"] < 0.7:
        return {
            "category": "",
            "manual": "",
            "info": "",
            "similar_input": "",
            "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
            "score": 0,
        }
    return res

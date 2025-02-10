import os
from typing import Dict, List

import pandas as pd
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# -------------------- 상수 및 설정 --------------------
# CSV 파일 경로 (실제 CSV 파일 위치에 맞게 수정하세요)
CSV_PATH = "data/manual.csv"
# 벡터스토어(DB) 저장 디렉토리 (변경사항이 적은 경우 재사용)
PERSIST_DIRECTORY = "chroma_db"


# -------------------- RAGRetriever 클래스 --------------------
class RAGRetriever:
    def __init__(self, path: str):
        self.path = path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

    def load_documents(self) -> List[Document]:
        """
        CSV 파일에서 문서를 읽어와 Document 객체 리스트로 반환합니다.
        """
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
            print(f"문서 로딩 중 에러 발생: {e}")
            raise

    def setup_retriever(self, docs: List[Document]) -> None:
        """
        persist directory에 저장된 벡터스토어가 있다면 재사용하고,
        없을 경우 새로 생성하여 저장합니다.
        """
        try:
            if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
                print(f"기존 벡터스토어 로드 중: {PERSIST_DIRECTORY}")
                self.vectorstore = Chroma(
                    persist_directory=PERSIST_DIRECTORY,
                    embedding_function=self.embeddings,
                    collection_name="rag-chroma",
                )
            else:
                print("새 벡터스토어 생성 중...")
                self.vectorstore = Chroma.from_documents(
                    documents=docs,
                    collection_name="rag-chroma",
                    embedding=self.embeddings,
                    persist_directory=PERSIST_DIRECTORY,
                )
                # Chroma 0.4.x 이후로는 자동으로 persist가 이루어지므로 별도 호출 불필요
        except Exception as e:
            print(f"리트리버 설정 중 에러 발생: {e}")
            raise

    def query(self, question: str) -> Dict:
        """
        사용자 질문에 대해 가장 유사한 문서를 검색하여 응답 정보를 반환합니다.
        """
        try:
            if not self.vectorstore:
                raise ValueError("Retriever가 초기화되지 않았습니다.")

            docs_with_scores = self.vectorstore.similarity_search_with_score(query=question, k=1)
            if not docs_with_scores:
                return {
                    "category": "",
                    "manual": "",
                    "info": "",
                    "similar_input": "",
                    "response": "해당 질문에 대한 답변을 찾을 수 없습니다.",
                    "score": 1.0,
                }

            doc, score = docs_with_scores[0]
            return {
                "category": doc.metadata.get("category", ""),
                "similar_input": doc.page_content,
                "manual": doc.metadata.get("manual", ""),
                "info": doc.metadata.get("info", ""),
                "response": doc.metadata.get("response", ""),
                "score": score,
            }
        except Exception as e:
            print(f"쿼리 실행 중 에러 발생: {e}")
            raise


# -------------------- 메인 함수 --------------------
def main():
    print("RAG 챗봇을 시작합니다. 종료하려면 'q' 또는 'quit'를 입력하세요.")
    print("=" * 50)

    # 문서 로딩 및 벡터스토어 설정
    retriever = RAGRetriever(CSV_PATH)
    documents = retriever.load_documents()
    retriever.setup_retriever(documents)

    # 사용자 입력을 통해 질의 수행
    while True:
        user_input = input("\n사용자: ").strip()
        if user_input.lower() in ["q", "quit", "종료"]:
            print("\n챗봇을 종료합니다.")
            break

        try:
            result = retriever.query(user_input)
            # score는 코사인 거리일 가능성이 있으므로 (1 - score)로 유사도를 계산
            similarity = 1 - result.get("score", 1.0)
            print("\n[답변]")
            print(f"카테고리: {result["category"]}")
            print(f"유사 질문: {result["similar_input"]}")
            print(f"유사도: {similarity:.4f}")
            print(f"답변: {result["response"]}")
            print("=" * 50)
        except Exception as e:
            print(f"오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()

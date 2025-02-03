from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
import pandas as pd

df = pd.read_csv("./data/aIcs-ace.csv")
df = df.dropna(subset=["분류", "input", "response"])
docs = []

for _, row in df.iterrows():
    doc = Document(
        page_content=row["input"],
        metadata={"분류": row["분류"], "response": row["response"]},
    )
    docs.append(doc)

vectorstore = Chroma.from_documents(
    documents=docs,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(),
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_input",
    "Get the most similar 'input' based on the question the user entered.",
)

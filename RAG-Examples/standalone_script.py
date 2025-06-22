"""
Simple RAG script: load a PDF, split into chunks, build/query a Chroma vector store,
then invoke ChatOllama to answer a query, cleaning out any <think> tags.
"""
import os
import json
import re
from uuid import uuid1
from pprint import pprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma


def load_and_split(pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 50):
    """
    Load PDF from path and split into text chunks.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


def create_vector_store(texts: list,
                        collection_name: str = "pdf_collection",
                        persist_dir: str = "./DB/chroma_langchain_db",
                        embed_model: str = "nomic-embed-text"):  
    """
    Build (or load) a Chroma vector store from document chunks.
    """
    os.makedirs(persist_dir, exist_ok=True)
    embeddings = OllamaEmbeddings(model=embed_model)
    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
    ids = [str(uuid1()) for _ in texts]
    vectordb.add_documents(documents=texts, ids=ids)
    return vectordb


def query_and_respond(vectordb: Chroma,
                      query: str,
                      chat_model: str = "deepseek-r1:1.5b") -> str:
    """
    Retrieve relevant docs and ask the LLM, removing any <think> tags from the answer.
    """
    retriever = vectordb.as_retriever()
    docs = retriever.invoke(query)

    context = [doc.page_content for doc in docs]
    prompt = json.dumps({
        "system": "You are a helpful assistant. Use the context below to answer the question.",
        "user": f"{query}\n\nContext:\n" + "\n".join(context)
    })

    llm = ChatOllama(model=chat_model)
    response = llm.invoke(prompt)
    # strip out any <think>...</think> blocks
    clean_text = re.sub(r'<think>.*?</think>', '', response.content, flags=re.DOTALL).strip()
    return clean_text


def main():
    # Configure paths and models
    pdf_path = "./files/Shishir-Resume-PD.pdf"
    query = "what did shishir do using Python"
    embed_model = "nomic-embed-text"
    chat_model = "deepseek-r1:1.5b"

    # Step 1: Load & split
    texts = load_and_split(pdf_path)

    # Step 2: Vector store
    vectordb = create_vector_store(
        texts,
        persist_dir="./DB/chroma_langchain_db",
        embed_model=embed_model
    )

    # Step 3: Query & respond
    answer = query_and_respond(vectordb, query, chat_model)

    pprint(answer)


if __name__ == "__main__":
    main()

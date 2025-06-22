import streamlit as st
import tempfile
import pandas as pd
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain.schema import Document
from uuid import uuid1
import json

# -- File Loading Helpers --
def write_to_temp(file) -> str:
    suffix = "." + file.name.split('.')[-1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(file.read())
    tmp.flush()
    return tmp.name


def load_file(file) -> list:
    ext = file.name.split('.')[-1].lower()
    temp_path = write_to_temp(file)
    try:
        if ext == 'pdf':
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
        elif ext in ('docx', 'doc'):
            loader = UnstructuredWordDocumentLoader(temp_path)
            docs = loader.load()
        elif ext in ('txt', 'text'):
            loader = TextLoader(temp_path)
            docs = loader.load()
        elif ext in ('xls', 'xlsx'):
            df = pd.read_excel(temp_path)
            text = df.astype(str).apply(lambda row: ' '.join(row.values), axis=1).str.cat(sep='\n')
            docs = [Document(page_content=text)]
        else:
            st.warning(f"Unsupported file type: {file.name}")
            return []
        return docs
    except Exception as e:
        st.error(f"Error loading {file.name}: {e}")
        return []

# -- Document Loading & Splitting --
@st.cache_data(show_spinner=False)
def load_and_split(files) -> list:
    all_docs = []
    for file in files:
        all_docs.extend(load_file(file))
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(all_docs)

# -- Vector Database Creation --
@st.cache_resource(show_spinner=False)
def create_vector_store(_texts: list):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectordb = Chroma(
        collection_name="pdf_collection",
        embedding_function=embeddings,
        persist_directory="./DB/chroma_langchain_db",
    )
    ids = [str(uuid1()) for _ in _texts]
    vectordb.add_documents(documents=_texts, ids=ids)
    return vectordb

# -- Query Processing & LLM Invocation --
def generate_response(query: str, docs: list, model_name: str) -> str:
    info = [doc.page_content for doc in docs]
    prompt = json.dumps({
        "system": "You are a helpful assistant, use the following context to answer the user.",
        "user": f"{query}\nRelated context:\n" + "\n".join(info)
    })
    llm = ChatOllama(model=model_name)
    result = llm.invoke(prompt)
    text = result.content
    # Remove any <think>...</think> tags and their content
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned.strip()

# -- Streamlit UI --
def main():
    st.title("📚 RAG Streamlit Demo")
    st.write("Upload one or more documents (PDF, DOCX, TXT, XLSX), build a vector store, and ask questions!")

    # Model selection dropdown
    available_models = ["gemma:2b", "gemma:7b", "deepseek-r1:1.5b", "deepseek-r1:latest"]
    model_name = st.selectbox(
        "Choose chat model:",
        options=available_models
    )
    st.session_state['model_name'] = model_name

    # Step 1: Document upload (multiple files)
    uploaded_files = st.file_uploader(
        "Choose documents", type=['pdf','docx','txt','xlsx','xls'], accept_multiple_files=True
    )
    if not uploaded_files:
        st.info("Please upload at least one document to get started.")
        return

    # Step 2: Load & split
    with st.expander("1️⃣ Load & Split Documents", expanded=True):
        if st.button("Load & Split"):
            with st.spinner("Processing documents..."):
                texts = load_and_split(uploaded_files)
            st.session_state['texts'] = texts
            st.success(f"Split into {len(texts)} chunks from {len(uploaded_files)} files.")

    # Step 3: Build Vector DB
    if 'texts' in st.session_state:
        with st.expander("2️⃣ Create Vector Database", expanded=True):
            if st.button("Build Vector Store"):
                with st.spinner("Creating vector database..."):
                    vectordb = create_vector_store(st.session_state['texts'])
                st.session_state['vectordb'] = vectordb
                st.success("Vector store ready.")

    # Step 4: Query Interface
    if 'vectordb' in st.session_state:
        with st.expander("3️⃣ Ask a Question", expanded=True):
            query = st.text_input("Enter your question:")
            if query and st.button("Get Answer"):
                if model_name not in available_models:
                    st.error(f"Model '{model_name}' is not available. Please select another model.")
                else:
                    with st.spinner("Retrieving relevant docs..."):
                        retriever = st.session_state['vectordb'].as_retriever()
                        docs = retriever.invoke(query)
                    with st.spinner("Generating response..."):
                        try:
                            answer = generate_response(query, docs, model_name)
                            st.subheader("Answer")
                            st.write(answer)
                        except Exception:
                            st.error(f"Failed to load model '{model_name}'. Please select another model.")

if __name__ == "__main__":
    main()

# RAG-Examples

This repository provides two tools for Retrieval-Augmented Generation (RAG):

1. **With Streamlit UI** (`streamlit_app.py`)  
2. **Standalone Script** (`rag_script.py`)

Users can upload one or more documents (PDF, DOCX, TXT, XLSX), build a local vector database, and ask natural-language questions via an Ollama LLM.

Project is Live at – _(replace with your deployment URL)_

## Features
- Upload SOP-style PDF, Word, text or Excel files  
- Splits large documents into manageable chunks  
- Builds a Chroma vector store with Ollama embeddings  
- Dropdown to select different Ollama models  
- Standalone CLI script for non-UI use

## Dependencies

- Python 3.7+  
- Streamlit  
- Pandas  
- OpenPyXL (for Excel)  
- python-docx (for Word)  
- PyPDF2 (for PDF loaders)  
- LangChain & community extensions  
- Ollama & Chroma connectors  
- ChromaDB

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/GenAI-Usecases.git
   cd GenAI-Usecases
   ```

## Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Configuration
1. Ollama
Ensure your Ollama daemon is running and models (e.g. gemma:2b, deepseek-r1:1.5b) are installed.

2. Persistence
By default, Chroma data is stored under ./DB/chroma_langchain_db. You can change this path in the scripts.

## Usage
1. Streamlit UI
    ```
    streamlit run streamlit_app.py
    ```
Open the provided URL in your browser.

Select your Ollama model from the dropdown.

Upload documents, split, build the vector store, then ask questions.

2. Standalone Script
    ```
    python3 rag_script.py
    ```
It will load ./files/Shishir-Resume-PD.pdf, build the DB, run a sample query, and print the response.

## Deployment
Self-Hosted: Serve behind your preferred web server or tunnel (e.g. ngrok) for external access.

## Notes
- Because this uses local Ollama models, ensure you have sufficient hardware and have pulled the models you intend to use.
- ChromaDB persistence may grow over time—clean or version your directories as needed.
- No external API keys are required beyond your own Ollama setup.

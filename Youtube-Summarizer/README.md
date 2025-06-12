# 🎬 YouTube Transcript Summarizer using Streamlit + Ollama + deepseek-r1:1.5b

This is a simple Streamlit-based web app that fetches the transcript of a YouTube video and summarizes it using a local Ollama LLM (Large Language Model) such as `deepseek-r1:1.5b`.

## 🚀 Features

- Paste any YouTube URL and fetch its transcript automatically
- Summarize long transcripts using Ollama's local LLM
- Clean and responsive UI built with Streamlit
- Model used: `deepseek-r1:1.5b` (you can change it)

---

## 🧰 Requirements

- Python 3.8+
- Ollama installed and running (with `deepseek-r1:1.5b` model pulled)
- Internet access to fetch video transcripts

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/youtube-transcript-summarizer.git
cd youtube-transcript-summarizer
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Pull the LLM model via Ollama (if not already)
```
ollama pull deepseek-r1:1.5b
```

### 4. Run the Streamlit app
```
streamlit run app.py
```

### Project Structure
```
.
├── app.py             # Streamlit application
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation

```
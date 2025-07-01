====================================================
🧠 RAG Chatbot with OpenAI / Gemini + Streamlit
====================================================

This is a **Retrieval-Augmented Generation (RAG)** chatbot that allows you to chat with your own documents (PDF, DOCX, PPTX, TXT). It uses OpenAI or Gemini models and provides a Streamlit-based UI for local use or desktop app mode.

----------------------------------------------------
✨ Features
----------------------------------------------------

- Chat with your uploaded documents using natural language
- Supports PDF, DOCX, PPTX, and TXT files
- Shows chat history in the session
- Works as a desktop or web app (Streamlit + pywebview)
- Embedding + context-aware answering with OpenAI or Gemini
- Uses ChromaDB as in-memory vector store

----------------------------------------------------
🧱 Tech Stack
----------------------------------------------------

Frontend      : Streamlit  
Backend       : Python  
LLM API       : OpenAI or Gemini  
Embeddings    : OpenAI/Gemini  
Vector Store  : ChromaDB  
File Parsing  : PyMuPDF, python-docx, pptx  
Desktop UI    : pywebview (optional)

----------------------------------------------------
⚙️ Setup and Installation
----------------------------------------------------

🔹 1. Prerequisites

- Python 3.8 or newer
- OpenAI or Gemini API key

🔹 2. Clone Repository

```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot

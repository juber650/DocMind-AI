# 🧠 DocMind AI

DocMind AI is a full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and interact with them through a modern web interface. Powered by local LLMs via Ollama, it ensures your data stays private and secure while providing accurate, context-aware answers complete with source page references.

---

## 🚀 Features

* **PDF Document Ingestion:** Upload any PDF to parse, split, and chunk text dynamically[cite: 3].
* **Local Vector Store:** Utilizes FAISS and HuggingFace embeddings (`sentence-transformers/all-MiniLM-L6-v2`) for fast and efficient semantic search[cite: 5].
* **Local LLM Integration:** Powered by Llama 3.2 (via Ollama) ensuring lightning-fast responses without relying on paid external cloud APIs[cite: 5].
* **Source Tracking:** Automatically extracts and displays page numbers and source filenames alongside AI answers[cite: 3].
* **Modern UI:** Built with Tailwind CSS and Markdown rendering for a clean, ChatGPT-like experience.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI, Python, Uvicorn[cite: 3]
* **RAG & Orchestration:** LangChain, LangChain Community, FAISS[cite: 5]
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)[cite: 5]
* **LLM Engine:** Ollama (`llama3.2:3b`)[cite: 5]
* **Frontend:** HTML5, Tailwind CSS, JavaScript, Marked.js

---

## ⚙️ Quick Start Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/DocMind-AI.git](https://github.com/your-username/DocMind-AI.git)
cd DocMind-AI

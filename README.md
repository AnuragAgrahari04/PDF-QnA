# 📚 PDF Question Answering App

An interactive web app that allows users to upload a PDF and ask questions about its content using **AI-powered language models**.

🔗 **Live Demo**: [https://pdf-qna-042004.streamlit.app/](https://pdf-qna-042004.streamlit.app/)

---

## 🚀 Features

- 📄 Upload any PDF file  
- ✂️ Automatically split and embed text using **Cohere Embeddings**  
- 🔍 Semantic search via **FAISS vector database**  
- 🤖 Get intelligent answers using **Cohere LLMs**  
- 🕘 View your question & answer history  
- 🧠 Powered by **LangChain**, **Streamlit**, and **Cohere**

---

## 🧑‍💻 Tech Stack

| Layer         | Technology                     |
|---------------|---------------------------------|
| Frontend      | Streamlit                      |
| Backend       | Python                         |
| Embeddings    | Cohere Embeddings              |
| Language Model| Cohere (`command` model)       |
| Vector DB     | FAISS                          |
| PDF Parsing   | PyMuPDF + LangChain Loader     |

---

## 🧠 How It Works

1. User uploads a PDF  
2. Text is extracted and split into chunks  
3. Each chunk is embedded with Cohere  
4. Chunks are indexed using FAISS  
5. On question input:
   - LangChain retrieves relevant chunks
   - Cohere LLM answers based on context

---

## 📥 Local Installation

```bash
git clone https://github.com/your-username/pdf-qna-app.git
cd pdf-qna-app
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```
## Add your Cohere API key
Create .streamlit/secrets.toml:

```bash

COHERE_API_KEY = "your_cohere_api_key"
```

## ▶️ Run Locally

```bash
streamlit run streamlit_app.py
```

## 🌐 Deploy to Streamlit Cloud
1. Push to GitHub

2. Go to Streamlit Cloud

3. Connect your repo

4. In App → Settings → Secrets, add:

```toml
COHERE_API_KEY = "your_cohere_api_key"
```

# HR Policy Chatbot (Streamlit + Chroma local + Ollama)

## Overview
Streamlit UI to upload PDF HR policies, embed them into a local Chroma DB, and answer employee HR queries using a local Ollama LLM via LangChain.

## Quickstart (recommended)
1. Create & activate a Python venv.
2. Install dependencies:
   pip install -r requirements.txt

3. Start Ollama (you must install Ollama per its docs; example):
   # start the REST server (default port 11434)
   ollama serve
   # pull a model you want to use (example)
   ollama pull llama3

   (See Ollama docs for platform-specific install & model names.) :contentReference[oaicite:5]{index=5}

4. Run Streamlit:
   streamlit run streamlit_app.py

5. Upload HR PDFs in the app, click "Ingest", then ask questions.

## Notes & tips
- If your PDFs are complex (tables, columns), consider installing `unstructured` and switching to `UnstructuredPDFLoader` in `vector_store.py`. :contentReference[oaicite:6]{index=6}
- For embeddings on CPU use a small sentence-transformers model like `all-MiniLM-L6-v2`. Using larger models on CPU will be slow. :contentReference[oaicite:7]{index=7}
- If you see LangChain deprecation warnings, make sure you installed the partner packages (`langchain-chroma`, `langchain-ollama`, `langchain-huggingface`, `langchain-text-splitters`). These were created to avoid import/deprecation churn.

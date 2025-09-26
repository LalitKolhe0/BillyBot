# streamlit_app.py

import streamlit as st
import tempfile
from vector_store import VectorStoreManager
from chatbot import answer_question

st.set_page_config(page_title=" Policy Chatbot", layout="wide")

st.title("🤖 Policy Chatbot (Ollama + Chroma)")

st.sidebar.header("Settings")
persist_dir = st.sidebar.text_input("Chroma persist directory", value="chroma_hr_db")
embedding_model = st.sidebar.text_input("Ollama embedding model", value="nomic-embed-text")
llm_model = st.sidebar.text_input("Ollama LLM model", value="llama3")
top_k = st.sidebar.slider("Top-k retrieved chunks", 1, 10, 4)
chunk_size = st.sidebar.number_input("Chunk size (chars)", value=1000)
chunk_overlap = st.sidebar.number_input("Chunk overlap (chars)", value=150)

@st.cache_resource
def get_manager():
    return VectorStoreManager(
        persist_directory=persist_dir,
        embedding_model=embedding_model,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

manager = get_manager()

st.header("1) Upload PDFs")
uploaded_files = st.file_uploader("Upload one or more HR policy PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Ingest uploaded PDFs into Chroma"):
        tmp_paths = []
        for f in uploaded_files:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(f.read())
            tmp.flush()
            tmp.close()
            tmp_paths.append(tmp.name)
        with st.spinner("Ingesting PDFs..."):
            try:
                db = manager.ingest_pdfs(tmp_paths, overwrite=False)
                st.success(f"Ingested {len(tmp_paths)} files into Chroma (persisted at {persist_dir}).")
            except Exception as e:
                st.error(f"Ingestion failed: {e}")

st.markdown("---")
st.header("2) Ask a question")
query = st.text_input("Type your question here (e.g., 'What is my sick leave policy?')")

if st.button("Ask") and query.strip():
    with st.spinner("Retrieving and answering..."):
        try:
            chroma_db = manager.load_chroma()
            resp = answer_question(query, chroma_db, top_k=top_k, model=llm_model)
            st.subheader("Answer")
            st.write(resp)
        except Exception as e:
            st.error(f"Query failed: {e}")

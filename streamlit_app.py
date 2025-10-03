"""
BillyBot Streamlit Interface - FIXED VERSION WITH WINDOWS SUPPORT
Replace your existing streamlit_app.py with this file
"""
import streamlit as st
import tempfile
import os
import shutil
import gc
import time
from pathlib import Path

# Import from local modules (works when run from project root)
try:
    from vector_store import VectorStoreManager
    from chatbot import answer_question
except ImportError:
    # Try importing from backend directory if running from root
    import sys
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    if os.path.exists(backend_path):
        sys.path.insert(0, backend_path)
        from vector_store import VectorStoreManager
        from chatbot import answer_question
    else:
        st.error("❌ Cannot find backend modules. Make sure you're running from the correct directory.")
        st.stop()

# Page configuration
st.set_page_config(
    page_title="BillyBot Policy Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1fae5;
        border: 1px solid #10b981;
        color: #065f46;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fee2e2;
        border: 1px solid #ef4444;
        color: #991b1b;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #dbeafe;
        border: 1px solid #3b82f6;
        color: #1e40af;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fef3c7;
        border: 1px solid #f59e0b;
        color: #92400e;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'manager' not in st.session_state:
    st.session_state.manager = None
if 'last_settings' not in st.session_state:
    st.session_state.last_settings = None

# Helper function to safely delete database (Windows-compatible)
def safe_delete_database(persist_dir, max_retries=3):
    """
    Safely delete database with retry logic for Windows file locking.
    
    Args:
        persist_dir: Directory to delete
        max_retries: Number of retry attempts
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # First, try to release the manager
    if st.session_state.manager:
        try:
            # Clear any references
            st.session_state.manager = None
            # Force garbage collection to release file handles
            gc.collect()
            time.sleep(0.5)  # Give OS time to release locks
        except Exception as e:
            st.warning(f"⚠️ Warning during cleanup: {e}")
    
    # Try to delete with retries
    for attempt in range(max_retries):
        try:
            if os.path.exists(persist_dir):
                # On Windows, try to handle read-only files
                def remove_readonly(func, path, exc_info):
                    """Error handler for Windows read-only files"""
                    os.chmod(path, 0o777)
                    func(path)
                
                shutil.rmtree(persist_dir, onerror=remove_readonly)
                return True, f"Successfully deleted {persist_dir}"
            else:
                return True, f"Directory {persist_dir} doesn't exist"
                
        except PermissionError as e:
            if attempt < max_retries - 1:
                # Wait and retry
                time.sleep(1)
                gc.collect()
                continue
            else:
                # Final attempt failed
                error_msg = f"""
                ⚠️ **Windows File Lock Issue**
                
                The database files are still in use. This can happen on Windows when:
                - The database was recently accessed
                - File handles haven't been released yet
                
                **Solutions:**
                1. Click the button again (files may be released now)
                2. Restart the Streamlit app: `Ctrl+C` then `streamlit run streamlit_app.py`
                3. Close all other apps that might be accessing the database
                
                **Error details:** {str(e)}
                """
                return False, error_msg
                
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    return False, "Failed after maximum retries"

# App header
st.markdown('<div class="main-header">🤖 BillyBot Policy Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Ollama + Chroma Vector Database</div>', unsafe_allow_html=True)

# Sidebar settings
st.sidebar.header("⚙️ Configuration")

# Database settings
st.sidebar.subheader("📊 Database Settings")
persist_dir = st.sidebar.text_input(
    "Chroma Directory",
    value="chroma_kb_db",
    help="Directory where vector embeddings are stored"
)

# Model settings
st.sidebar.subheader("🤖 Model Settings")
embedding_model = st.sidebar.text_input(
    "Embedding Model",
    value="nomic-embed-text",
    help="Ollama model for creating embeddings"
)
llm_model = st.sidebar.text_input(
    "LLM Model",
    value="llama3",
    help="Ollama model for generating responses"
)

# Retrieval settings
st.sidebar.subheader("🔍 Retrieval Settings")
top_k = st.sidebar.slider(
    "Top-K Chunks",
    min_value=1,
    max_value=10,
    value=4,
    help="Number of relevant chunks to retrieve"
)

# Chunking settings
st.sidebar.subheader("📄 Chunking Settings")
chunk_size = st.sidebar.number_input(
    "Chunk Size",
    min_value=500,
    max_value=3000,
    value=1000,
    step=100,
    help="Characters per document chunk"
)
chunk_overlap = st.sidebar.number_input(
    "Chunk Overlap",
    min_value=0,
    max_value=500,
    value=150,
    step=50,
    help="Overlapping characters between chunks"
)

# Create current settings dict
current_settings = {
    'persist_dir': persist_dir,
    'embedding_model': embedding_model,
    'chunk_size': chunk_size,
    'chunk_overlap': chunk_overlap
}

# Check if settings changed
settings_changed = st.session_state.last_settings != current_settings

# Initialize or update manager
if st.session_state.manager is None or settings_changed:
    try:
        st.session_state.manager = VectorStoreManager(
            persist_directory=persist_dir,
            embedding_model=embedding_model,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        st.session_state.last_settings = current_settings
        if settings_changed and st.session_state.last_settings is not None:
            st.sidebar.success("✓ Settings updated!")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to initialize manager: {str(e)}")
        st.stop()

manager = st.session_state.manager

# System status
st.sidebar.markdown("---")
st.sidebar.subheader("📊 System Status")
if os.path.exists(persist_dir):
    st.sidebar.success(f"✓ Database exists: `{persist_dir}`")
else:
    st.sidebar.warning(f"⚠️ Database not found: `{persist_dir}`")

st.sidebar.info(f"📦 Embedding Model: `{embedding_model}`")
st.sidebar.info(f"🧠 LLM Model: `{llm_model}`")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload PDFs", "💬 Ask Questions", "🗑️ Database Management"])

# Tab 1: Upload PDFs
with tab1:
    st.header("📤 Upload PDF Documents")
    st.write("Upload one or more PDF files to add them to your knowledge base.")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Select one or more PDF files to upload"
    )
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} file(s) selected:**")
        for file in uploaded_files:
            st.write(f"- {file.name} ({file.size / 1024:.2f} KB)")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            ingest_button = st.button("🚀 Ingest PDFs into Chroma", type="primary", use_container_width=True)
        with col2:
            overwrite = st.checkbox("Overwrite", value=False, help="Clear existing database before ingesting")
        
        if ingest_button:
            tmp_paths = []
            try:
                # Save uploaded files temporarily
                with st.spinner("💾 Saving files..."):
                    for f in uploaded_files:
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        tmp.write(f.read())
                        tmp.flush()
                        tmp.close()
                        tmp_paths.append(tmp.name)
                
                # Ingest PDFs
                with st.spinner(f"🔄 Processing {len(tmp_paths)} PDF(s)... This may take a while."):
                    db = manager.ingest_pdfs(tmp_paths, overwrite=overwrite)
                    
                st.markdown(f"""
                <div class="success-box">
                    <h4>✅ Success!</h4>
                    <p>Ingested {len(tmp_paths)} file(s) into Chroma database.</p>
                    <p>Location: <code>{persist_dir}</code></p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    <h4>❌ Ingestion Failed</h4>
                    <p>{str(e)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            finally:
                # Clean up temporary files
                for tmp_path in tmp_paths:
                    try:
                        os.unlink(tmp_path)
                    except Exception as e:
                        st.warning(f"Could not delete temp file: {e}")
    
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <strong>💡 Tips:</strong>
        <ul>
            <li>Upload well-formatted PDF files for best results</li>
            <li>Multiple files can be uploaded at once</li>
            <li>Documents are automatically chunked and embedded</li>
            <li>Check "Overwrite" to replace existing database</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Ask Questions
with tab2:
    st.header("💬 Ask Questions")
    st.write("Type your question about the uploaded documents and get AI-powered answers.")
    
    # Check if database exists
    if not os.path.exists(persist_dir):
        st.warning("⚠️ No database found. Please upload PDF files first in the 'Upload PDFs' tab.")
    else:
        # Question input
        query = st.text_input(
            "Your Question:",
            placeholder="e.g., What is the company policy on remote work?",
            help="Ask anything about your uploaded documents"
        )
        
        col1, col2 = st.columns([4, 1])
        with col1:
            ask_button = st.button("🔍 Ask Question", type="primary", use_container_width=True)
        with col2:
            clear_chat = st.button("🗑️ Clear Chat", use_container_width=True)
        
        if clear_chat:
            st.session_state.chat_history = []
            st.rerun()
        
        if ask_button and query.strip():
            try:
                # Add user message to chat
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': query
                })
                
                with st.spinner("🤔 Thinking..."):
                    # Load database and get answer
                    chroma_db = manager.load_chroma()
                    response = answer_question(
                        query,
                        chroma_db,
                        top_k=top_k,
                        model=llm_model
                    )
                    
                    # Add assistant response to chat
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                    
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Query failed: {str(e)}")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.subheader("📜 Conversation History")
            
            for i, message in enumerate(st.session_state.chat_history):
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="background-color: #e0f2fe; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                        <strong>👤 You:</strong><br/>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                        <strong>🤖 BillyBot:</strong><br/>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)

# Tab 3: Database Management
with tab3:
    st.header("🗑️ Database Management")
    st.write("Manage your vector database and view storage information.")
    
    # Database info
    if os.path.exists(persist_dir):
        db_path = Path(persist_dir)
        
        # Calculate database size
        try:
            total_size = sum(f.stat().st_size for f in db_path.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            
            st.markdown(f"""
            <div class="info-box">
                <h4>📊 Database Information</h4>
                <ul>
                    <li><strong>Location:</strong> <code>{persist_dir}</code></li>
                    <li><strong>Size:</strong> {size_mb:.2f} MB</li>
                    <li><strong>Embedding Model:</strong> {embedding_model}</li>
                    <li><strong>Chunk Size:</strong> {chunk_size} characters</li>
                    <li><strong>Chunk Overlap:</strong> {chunk_overlap} characters</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not calculate database size: {e}")
    else:
        st.info("ℹ️ No database found. Upload PDFs to create one.")
    
    st.markdown("---")
    
    # Windows-specific warning
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Windows Users:</strong> If deletion fails, the database files may still be in use. 
        Try clicking the delete button again, or restart the Streamlit app.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Clear database section
    st.subheader("⚠️ Danger Zone")
    st.write("Permanently delete the vector database. This action cannot be undone.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        confirm_text = st.text_input(
            "Type 'DELETE' to confirm:",
            placeholder="DELETE",
            help="Type DELETE in all caps to enable the delete button"
        )
    with col2:
        delete_enabled = confirm_text == "DELETE"
        delete_button = st.button(
            "🗑️ Clear Database",
            type="secondary",
            disabled=not delete_enabled,
            use_container_width=True
        )
    
    if delete_button and delete_enabled:
        with st.spinner("🗑️ Clearing database..."):
            success, message = safe_delete_database(persist_dir)
            
            if success:
                # Clear session state
                st.session_state.manager = None
                st.session_state.chat_history = []
                
                st.markdown(f"""
                <div class="success-box">
                    <h4>✅ Database Cleared</h4>
                    <p>{message}</p>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(1)
                st.rerun()
            else:
                st.markdown(f"""
                <div class="error-box">
                    <h4>❌ Failed to Clear Database</h4>
                    <p>{message}</p>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
    <p>🤖 BillyBot Policy Chatbot | Powered by Ollama & Chroma</p>
    <p>Make sure Ollama is running with the required models installed</p>
</div>
""", unsafe_allow_html=True)
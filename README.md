# BillyBot - HR Policy Chatbot

A modern HR policy chatbot with both React frontend and Streamlit interfaces, built with Ollama and Chroma for document retrieval and question answering.

## Features

- 🤖 **AI-Powered Chat**: Ask questions about HR policies using Ollama LLM
- 📄 **PDF Upload**: Drag-and-drop interface for uploading policy documents
- ⚙️ **Configurable Settings**: Adjust models, chunk sizes, and retrieval parameters
- 🎨 **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- 🔍 **Vector Search**: Powered by Chroma for semantic document retrieval
- 📱 **Multiple Interfaces**: Both React frontend and Streamlit app available

## Architecture

- **Frontend**: React with Tailwind CSS
- **Backend**: FastAPI with Python
- **AI**: Ollama for embeddings and LLM
- **Vector Store**: Chroma for document storage and retrieval
- **Alternative UI**: Streamlit app for quick setup

## Quick Start

### Prerequisites

- Node.js 16+ and npm (for React frontend)
- Python 3.8+
- Ollama installed and running
- Required Ollama models: `nomic-embed-text` and `llama3`

### Option 1: React Frontend (Recommended)

1. **Install Ollama models**:
   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3
   ```

2. **Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

3. **Setup Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Option 2: Streamlit App (Quick Setup)

1. **Create a virtual environment and activate it**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   .\venv\Scripts\python.exe -m pip install --upgrade pip
   .\venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. **Install additional packages for document processing**:
   ```powershell
   .\venv\Scripts\python.exe -m pip install "unstructured[all-docs]"
   ```

4. **Run the Streamlit app**:
   ```powershell
   .\venv\Scripts\python.exe -m streamlit run app/streamlit_app.py --server.headless true
   ```

## Usage

### React Frontend
1. **Upload PDFs**: Go to the "Upload PDFs" tab and drag-and-drop your HR policy documents
2. **Configure Settings**: Adjust model settings, chunk sizes, and retrieval parameters in the sidebar
3. **Ask Questions**: Switch to the "Ask Questions" tab and start chatting with the AI about your policies

### Streamlit App
1. **Upload Documents**: Use the file uploader to add HR policy documents
2. **Ask Questions**: Type your questions in the chat interface
3. **Configure Settings**: Adjust model and retrieval parameters as needed

## API Endpoints

- `GET /health` - Health check
- `POST /upload` - Upload and ingest PDF files
- `POST /ask` - Ask questions about uploaded documents

## Development

### Frontend Development
```bash
cd frontend
npm start
```

### Backend Development
```bash
cd backend
uvicorn main:app --reload
```

### Streamlit Development
```bash
python -m streamlit run app/streamlit_app.py
```

## Configuration

The application supports various configuration options:

- **Models**: Choose different Ollama models for embeddings and LLM
- **Chunk Size**: Adjust document chunk size for processing
- **Chunk Overlap**: Set overlap between chunks
- **Top-k**: Number of relevant chunks to retrieve
- **Persist Directory**: Location for Chroma database storage

## Troubleshooting

### Common Error: ModuleNotFoundError: No module named 'unstructured'

**Symptoms**: Traceback shows `ModuleNotFoundError: No module named 'unstructured'` coming from `langchain_community.document_loaders`.

**Fix**:
```powershell
.\venv\Scripts\python.exe -m pip install "unstructured[all-docs]"
```

### Other Common Issues

- Missing OpenAI / Hugging Face keys: set `OPENAI_API_KEY` or `HUGGINGFACEHUB_API_TOKEN` in your environment or `.env` file
- LangChain deprecation warnings: they are warnings; the app should still run
- Chromadb persistence errors: some Chroma wrappers don't expose `.persist()` — the code already handles this

## Project Structure

### React Frontend
- `frontend/` - React application with Tailwind CSS
- `backend/` - FastAPI backend
- `app/` - Streamlit application

### Key Files
- `app/streamlit_app.py` — Streamlit UI and app entrypoint
- `backend/main.py` — FastAPI backend
- `frontend/src/` — React frontend source
- `src/vector_store.py` — Vector DB manager (Chroma or FAISS) and embeddings setup
- `src/chatbot.py` — Chat wrapper that calls the LLM
- `data/` — Place to add HR documents

## 🚀 Deployment

### GitHub Hosting

1. **Create a new repository** on GitHub
2. **Clone and push** your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: BillyBot HR Policy Chatbot"
   git branch -M main
   git remote add origin https://github.com/yourusername/billybot.git
   git push -u origin main
   ```

3. **Enable GitHub Pages** (for frontend):
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: main, folder: /frontend/build

### 🐳 Docker Deployment

**Local Docker deployment**:
```bash
# Windows
deploy.bat

# Linux/Mac
chmod +x deploy.sh
./deploy.sh
```

**Production deployment**:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Tests

Run tests with pytest:
```powershell
.\venv\Scripts\python.exe -m pytest -q
```

## Future Enhancements

1. Option for selecting models or LLMs through API integration
2. Identity access management - User Role definition
3. Settings or Configuration pages for this
4. VectorDB from cloud
5. Folder to upload docs (Or List of docs uploaded can be seen)
6. Enhanced UI in React
7. Multi-language support
8. Advanced analytics and reporting

## License

MIT License - see LICENSE file for details.
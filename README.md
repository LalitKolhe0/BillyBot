# BillyBot - Policy Chatbot

A modern React frontend for the BillyBot Policy Chatbot, built with Ollama and Chroma for document retrieval and question answering.

## Features

- 🤖 **AI-Powered Chat**: Ask questions about HR policies using Ollama LLM
- 📄 **PDF Upload**: Drag-and-drop interface for uploading policy documents
- ⚙️ **Configurable Settings**: Adjust models, chunk sizes, and retrieval parameters
- 🎨 **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- 🔍 **Vector Search**: Powered by Chroma for semantic document retrieval

## Architecture

- **Frontend**: React with Tailwind CSS
- **Backend**: FastAPI with Python
- **AI**: Ollama for embeddings and LLM
- **Vector Store**: Chroma for document storage and retrieval

## Quick Start

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Ollama installed and running
- Required Ollama models: `nomic-embed-text` and `llama3`

### Installation

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

## Usage

1. **Upload PDFs**: Go to the "Upload PDFs" tab and drag-and-drop your HR policy documents
2. **Configure Settings**: Adjust model settings, chunk sizes, and retrieval parameters in the sidebar
3. **Ask Questions**: Switch to the "Ask Questions" tab and start chatting with the AI about your policies

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

## Configuration

The application supports various configuration options:

- **Models**: Choose different Ollama models for embeddings and LLM
- **Chunk Size**: Adjust document chunk size for processing
- **Chunk Overlap**: Set overlap between chunks
- **Top-k**: Number of relevant chunks to retrieve
- **Persist Directory**: Location for Chroma database storage

## 🚀 GitHub Hosting

### Quick Deploy to GitHub

1. **Create a new repository** on GitHub
2. **Clone and push** your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: BillyBot React frontend"
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

### 🔄 CI/CD Pipeline

The repository includes GitHub Actions for:
- ✅ Automated testing
- 🏗️ Docker image building
- 🚀 Deployment automation

### 📦 Containerization

- **Dockerfile**: Multi-stage build for production
- **docker-compose.yml**: Local development setup
- **nginx.conf**: Reverse proxy configuration

## License

MIT License - see LICENSE file for details.
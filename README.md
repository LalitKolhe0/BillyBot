# 🤖 BillyBot - RAG-Based Policy Chatbot

A powerful Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Ollama, and ChromaDB. Upload PDF documents and ask questions about their content using state-of-the-art local LLMs.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Demo](#-demo)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- 📄 **PDF Document Processing** - Upload and process multiple PDF files
- 🔍 **Semantic Search** - Retrieve relevant context using vector embeddings
- 💬 **Intelligent Q&A** - Get accurate answers from your documents
- 🗄️ **Persistent Vector Store** - ChromaDB for efficient storage and retrieval
- 🤖 **Local LLM** - Powered by Ollama (no API keys needed!)

### Two User Interfaces
- **React Frontend** - Modern, responsive UI with drag-and-drop
- **Streamlit Interface** - Simple, all-in-one alternative with chat history

### Advanced Features
- ⚙️ **Configurable Settings** - Adjust models, chunk sizes, and retrieval parameters
- 🔄 **Real-time Processing** - Instant feedback on uploads and queries
- 🧹 **Database Management** - Clear and reset vector database easily
- 📊 **Source Citations** - Answers include source document references
- 🎨 **Beautiful UI** - Tailwind CSS styling with intuitive design

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │   React Frontend     │      │ Streamlit Interface  │    │
│  │  (Port 3000)         │      │  (Port 8501)         │    │
│  └──────────┬───────────┘      └──────────┬───────────┘    │
└─────────────┼────────────────────────────┼─────────────────┘
              │                            │
              │         REST API           │
              │                            │
┌─────────────▼────────────────────────────▼─────────────────┐
│                   FastAPI Backend                           │
│                    (Port 8000)                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Vector Store Manager                    │   │
│  │  • PDF Processing (PyPDF)                           │   │
│  │  • Text Chunking (LangChain)                        │   │
│  │  • Embedding Generation (Ollama)                    │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────┬──────────────────────────┬──────────────────┘
               │                          │
               ▼                          ▼
    ┌──────────────────┐      ┌──────────────────────┐
    │   ChromaDB       │      │    Ollama Server     │
    │ (Vector Store)   │      │   (LLM & Embeddings) │
    │                  │      │                      │
    │ • Embeddings     │      │ • nomic-embed-text   │
    │ • Metadata       │      │ • llama3             │
    │ • Persistence    │      │ • Local inference    │
    └──────────────────┘      └──────────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI - Modern async web framework
- LangChain - LLM application framework
- ChromaDB - Vector database
- Ollama - Local LLM inference
- PyPDF - PDF text extraction

**Frontend (React):**
- React 18 - UI framework
- Tailwind CSS - Styling
- Axios - HTTP client
- Lucide React - Icons
- React Dropzone - File uploads

**Alternative Interface:**
- Streamlit - Rapid prototyping framework

---

## 🎬 Demo

### React Interface
![React Interface](docs/images/react-interface.png)

### Streamlit Interface
![Streamlit Interface](docs/images/streamlit-interface.png)

*(Add screenshots of your application here)*

---

## 📦 Prerequisites

Before installation, ensure you have:

- **Python 3.8 or higher**
  ```bash
  python --version
  ```

- **Node.js 16 or higher** (for React frontend)
  ```bash
  node --version
  ```

- **Ollama** ([Download here](https://ollama.ai))
  ```bash
  ollama --version
  ```

- **Git** (for cloning the repository)
  ```bash
  git --version
  ```

---

## 🚀 Installation

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/billybot.git
cd billybot

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Install Ollama models
ollama pull nomic-embed-text
ollama pull llama3

# 4. Frontend setup (optional, for React interface)
cd ../frontend
npm install
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# 5. Run the application
# Option A: React + FastAPI
cd ../backend && python main.py  # Terminal 1
cd frontend && npm start          # Terminal 2

# Option B: Streamlit (simpler)
streamlit run streamlit_app.py
```

### Detailed Installation

See [INSTALLATION.md](docs/INSTALLATION.md) for detailed setup instructions.

---

## 💻 Usage

### Using the React Interface

1. **Start the backend:**
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```
   Backend will run on http://localhost:8000

2. **Start the frontend:**
   ```bash
   cd frontend
   npm start
   ```
   Frontend will open at http://localhost:3000

3. **Upload PDFs:**
   - Drag and drop PDF files or click to browse
   - Click "Upload Files" button
   - Wait for processing to complete

4. **Ask Questions:**
   - Switch to "Ask Questions" tab
   - Type your question in the input field
   - Click "Ask" or press Enter
   - View the AI-generated answer with sources

### Using the Streamlit Interface

1. **Run Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```
   App will open at http://localhost:8501

2. **Configure Settings:**
   - Adjust settings in the sidebar
   - Choose models, chunk sizes, etc.

3. **Upload and Query:**
   - Use "Upload PDFs" tab to add documents
   - Use "Ask Questions" tab for Q&A
   - Use "Database Management" to view/clear data

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Backend Settings

Configurable via UI or API requests:

| Setting | Default | Description |
|---------|---------|-------------|
| `persistDir` | `chroma_kb_db` | Vector database directory |
| `embeddingModel` | `nomic-embed-text` | Ollama embedding model |
| `llmModel` | `llama3` | Ollama LLM model |
| `topK` | `4` | Number of chunks to retrieve |
| `chunkSize` | `1000` | Characters per chunk |
| `chunkOverlap` | `150` | Overlap between chunks |

### Recommended Models

**Embedding Models:**
- `nomic-embed-text` - Best balance (default)
- `mxbai-embed-large` - Higher quality
- `all-minilm` - Faster, smaller

**LLM Models:**
- `llama3` - Best quality (default)
- `llama2` - Good alternative
- `mistral` - Faster responses
- `phi3` - Lightweight

Install with: `ollama pull <model-name>`

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "BillyBot API is running"
}
```

#### Upload Files
```http
POST /upload
Content-Type: multipart/form-data
```

**Parameters:**
- `files`: PDF file(s) to upload
- `settings`: JSON string with configuration

**Response:**
```json
{
  "message": "Successfully ingested 2 files into Chroma database",
  "files_processed": 2,
  "persist_directory": "chroma_kb_db"
}
```

#### Ask Question
```http
POST /ask
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "What is the policy on remote work?",
  "settings": {
    "topK": 4,
    "llmModel": "llama3"
  }
}
```

**Response:**
```json
{
  "answer": "According to the company policy...",
  "question": "What is the policy on remote work?"
}
```

#### Clear Database
```http
DELETE /clear-database
```

**Response:**
```json
{
  "message": "Database cleared successfully",
  "cleared_directories": ["chroma_kb_db"],
  "status": "success"
}
```

#### System Status
```http
GET /status
```

**Response:**
```json
{
  "database_loaded": true,
  "persist_directory": "chroma_kb_db",
  "embedding_model": "nomic-embed-text"
}
```

### Interactive API Docs

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📁 Project Structure

```
billybot/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── vector_store.py         # Vector database manager
│   ├── chatbot.py              # LLM chatbot logic
│   ├── requirements.txt        # Python dependencies
│   └── chroma_kb_db/          # Vector database (created on first upload)
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.js       # App header
│   │   │   ├── SettingsPanel.js # Settings sidebar
│   │   │   ├── FileUpload.js   # PDF upload component
│   │   │   └── ChatInterface.js # Chat UI
│   │   ├── context/
│   │   │   └── SettingsContext.js # Global settings
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── App.js              # Main component
│   │   └── index.js            # Entry point
│   ├── package.json            # Node dependencies
│   └── .env                    # Environment variables
│
├── streamlit_app.py            # Alternative Streamlit interface
├── README.md                   # This file
├── INSTALLATION.md             # Detailed setup guide
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore rules
```

---

## 🐛 Troubleshooting

### Common Issues

#### Backend won't start

**Error:** `ModuleNotFoundError`
```bash
# Solution: Activate virtual environment and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

**Error:** `Port 8000 already in use`
```bash
# Solution: Kill the process or use a different port
lsof -ti:8000 | xargs kill -9
# Or change port in main.py
```

#### Frontend won't connect

**Error:** CORS errors
```bash
# Solution: Ensure backend is running and CORS is configured
# Check backend terminal for startup messages
```

**Error:** `REACT_APP_API_URL is not defined`
```bash
# Solution: Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env
npm start
```

#### Ollama issues

**Error:** `Connection refused`
```bash
# Solution: Start Ollama
ollama serve
```

**Error:** `Model not found`
```bash
# Solution: Pull the model
ollama pull nomic-embed-text
ollama pull llama3
```

#### Upload fails

**Error:** `No database loaded`
```bash
# Solution: This is normal on first run. Upload files will create the database.
```

**Error:** PDF processing fails
```bash
# Solution: Ensure PDF is not corrupted and is text-based (not scanned images)
```

### Getting Help

1. Check the [Issues](https://github.com/lalitkolhe0/billybot/issues) page
2. Review the [Installation Guide](docs/INSTALLATION.md)



## 🗺️ Roadmap

### Planned Features

- [ ] User authentication and multi-user support
- [ ] Support for more file types (DOCX, TXT, Markdown)
- [ ] Chat history persistence in database
- [ ] Export conversations to PDF/Markdown
- [ ] Advanced search filters and faceting
- [ ] Batch question processing
- [ ] Docker deployment setup
- [ ] Multi-language support
- [ ] Custom prompt templates
- [ ] Integration with cloud storage (S3, Google Drive)

### Version History

**v0.1.0** (Current)
- Initial release
- PDF upload and processing
- React and Streamlit interfaces
- Basic Q&A functionality
- ChromaDB vector storage
- Ollama integration

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 BillyBot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

Built with amazing open-source technologies:

- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [Ollama](https://ollama.ai) - Local LLM inference
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [React](https://reactjs.org/) - UI library
- [Streamlit](https://streamlit.io/) - Data apps framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

Special thanks to the open-source community! 💙

---
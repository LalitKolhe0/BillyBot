# BillyBot Backend

FastAPI backend for the BillyBot Policy Chatbot.

## Features

- 🚀 FastAPI with async support
- 📄 PDF processing and ingestion
- 🤖 Ollama integration for embeddings and LLM
- 🗄️ Chroma vector database
- 🔄 CORS support for frontend integration

## Getting Started

### Prerequisites

- Python 3.8+
- Ollama installed and running
- Required Ollama models: `nomic-embed-text` and `llama3`

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /health
```

### Upload Files
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- files: List of PDF files
- settings: JSON string with configuration
```

### Ask Question
```
POST /ask
Content-Type: application/x-www-form-urlencoded

Parameters:
- question: String question
- settings: JSON string with configuration
```

## Configuration

The backend accepts the following settings:

- `persistDir`: Chroma database directory
- `embeddingModel`: Ollama embedding model name
- `llmModel`: Ollama LLM model name
- `topK`: Number of chunks to retrieve
- `chunkSize`: Document chunk size
- `chunkOverlap`: Overlap between chunks

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- LangChain: LLM framework
- Chroma: Vector database
- Ollama: Local LLM integration
- PyPDF: PDF processing

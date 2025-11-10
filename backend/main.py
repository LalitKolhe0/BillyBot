from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import json
from typing import List
import uvicorn
import shutil

from vector_store import VectorStoreManager
from chatbot import answer_question


app = FastAPI(title="BillyBot API", version="1.0.0")

# CORS middleware - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global manager instance
manager = None



@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "BillyBot API is running"}


@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    settings: str = Form(...)
):
    """
    Upload and ingest PDF files into the vector database
    """
    global chroma_db 
    global manager
    
    temp_paths = []
    try:
        # Parse settings
        settings_dict = json.loads(settings)
        
        # Initialize manager with settings
        manager = VectorStoreManager(
            persist_directory=settings_dict.get("persistDir", "chroma_kb_db"),
            embedding_model=settings_dict.get("embeddingModel", "nomic-embed-text"),
            chunk_size=settings_dict.get("chunkSize", 1000),
            chunk_overlap=settings_dict.get("chunkOverlap", 150),
        )
        chroma_db = None
        
        # Save uploaded files temporarily
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail=f"Only PDF files are allowed. Got: {file.filename}")
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
            temp_paths.append(temp_file.name)

        # Ingest PDFs
        db = manager.ingest_pdfs(temp_paths, overwrite=False)
        
        # Clean up temporary files
        for temp_path in temp_paths:
            try:
                os.unlink(temp_path)
            except Exception as e:
                print(f"Warning: Failed to delete temp file {temp_path}: {e}")
        
        return {
            "message": f"Successfully ingested {len(files)} files into Chroma database",
            "files_processed": len(files),
            "persist_directory": manager.persist_directory
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid settings JSON")
    except Exception as e:
        # Clean up temporary files on error
        for temp_path in temp_paths:
            try:
                os.unlink(temp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/ask")
async def ask_question_endpoint(request: dict):
    """
    Ask a question to the chatbot
    """
    global manager
    
    if not manager:
        raise HTTPException(
            status_code=400, 
            detail="No database loaded. Please upload files first."
        )
    
    try:
        # Extract question and settings from request
        question = request.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
            
        settings_dict = request.get("settings", {})
        
        # Load Chroma database
        global chroma_db
        if not chroma_db:
            chroma_db = manager.load_chroma()
        
                
        # Get answer
        answer = answer_question(
            question, 
            chroma_db, 
            top_k=settings_dict.get("topK", 4),
            model=settings_dict.get("llmModel", "llama3")
        )
        
        return {
            "answer": answer,
            "question": question
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.delete("/clear-database")
async def clear_database():
    """
    Clear all vector database directories
    """
    global manager
    
    try:
        # List of all possible database directories to clear
        directories_to_clear = [ ]
        
        # If manager exists, add its persist directory and reset it
        if manager:
            directories_to_clear.append(manager.persist_directory)
            manager = None  # Reset the manager
        else:
            directories_to_clear.append("chroma_kb_db")
        
        # Remove duplicates and clear all directories
        cleared_dirs = []
        for directory in set(directories_to_clear):
            if os.path.exists(directory):
                try:
                    shutil.rmtree(directory)
                    cleared_dirs.append(directory)
                    print(f"✓ Cleared directory: {directory}")
                except Exception as e:
                    print(f"✗ Failed to clear {directory}: {e}")
        
        if cleared_dirs:
            return {
                "message": f"Database cleared successfully",
                "cleared_directories": cleared_dirs,
                "status": "success"
            }
        else:
            return {
                "message": "No database directories found to clear",
                "status": "info"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to clear database: {str(e)}"
        )


@app.get("/status")
async def get_status():
    """
    Get current system status
    """
    global manager
    
    return {
        "database_loaded": manager is not None,
        "persist_directory": manager.persist_directory if manager else None,
        "embedding_model": manager.embedding_model if manager else None
    }


if __name__ == "__main__":
    print("🚀 Starting BillyBot API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
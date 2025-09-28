from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
import json
from typing import List
import uvicorn

from vector_store import VectorStoreManager
from chatbot import answer_question

app = FastAPI(title="BillyBot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global manager instance
manager = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "BillyBot API is running"}

@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    settings: str = Form(...)
):
    global manager
    
    try:
        # Parse settings
        settings_dict = json.loads(settings)
        
        # Initialize manager with settings
        manager = VectorStoreManager(
            persist_directory=settings_dict.get("persistDir", "chroma_hr_db"),
            embedding_model=settings_dict.get("embeddingModel", "nomic-embed-text"),
            chunk_size=settings_dict.get("chunkSize", 1000),
            chunk_overlap=settings_dict.get("chunkOverlap", 150),
        )
        
        # Save uploaded files temporarily
        temp_paths = []
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
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
            except:
                pass
        
        return {
            "message": f"Successfully ingested {len(files)} files into Chroma database",
            "files_processed": len(files)
        }
        
    except Exception as e:
        # Clean up temporary files on error
        for temp_path in temp_paths:
            try:
                os.unlink(temp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question_endpoint(request: dict):
    global manager
    
    if not manager:
        raise HTTPException(status_code=400, detail="No database loaded. Please upload files first.")
    
    try:
        # Extract question and settings from request
        question = request.get("question")
        settings_dict = request.get("settings", {})
        
        # Load Chroma database
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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

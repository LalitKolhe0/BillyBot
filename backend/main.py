from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import tempfile
import os
import json
from typing import List
import uvicorn
from datetime import timedelta
from sqlalchemy.orm import Session

from vector_store import VectorStoreManager
from chatbot import answer_question
from database import get_db, engine
from models import Base, User
from schemas import UserCreate, UserLogin, UserResponse, Token
from auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from oauth_config import google_oauth, facebook_oauth, apple_oauth, GOOGLE_SCOPES, FACEBOOK_SCOPES, APPLE_SCOPES
from oauth_service import create_or_get_social_user, get_social_user_info

# Create database tables
Base.metadata.create_all(bind=engine)

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

# Authentication endpoints
@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token."""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

# OAuth2 Social Authentication Endpoints
@app.get("/auth/google")
async def google_login():
    """Initiate Google OAuth2 login."""
    redirect_uri = google_oauth.get_authorize_url(
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback/google"),
        scope=GOOGLE_SCOPES
    )
    return {"auth_url": redirect_uri}

@app.get("/auth/facebook")
async def facebook_login():
    """Initiate Facebook OAuth2 login."""
    redirect_uri = facebook_oauth.get_authorize_url(
        redirect_uri=os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:3000/auth/callback/facebook"),
        scope=FACEBOOK_SCOPES
    )
    return {"auth_url": redirect_uri}

@app.get("/auth/apple")
async def apple_login():
    """Initiate Apple OAuth2 login."""
    redirect_uri = apple_oauth.get_authorize_url(
        redirect_uri=os.getenv("APPLE_REDIRECT_URI", "http://localhost:3000/auth/callback/apple"),
        scope=APPLE_SCOPES
    )
    return {"auth_url": redirect_uri}

@app.post("/auth/callback/google", response_model=Token)
async def google_callback(code: str, db: Session = Depends(get_db)):
    """Handle Google OAuth2 callback."""
    try:
        # Exchange code for token
        token = google_oauth.get_access_token(
            code=code,
            redirect_uri=os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback/google")
        )
        
        # Get user info from Google
        user_info = google_oauth.get_user_info(token=token)
        
        # Extract user data
        user_data = get_social_user_info("google", user_info)
        
        # Create or get user
        user = create_or_get_social_user(
            db=db,
            email=user_data["email"],
            provider="google",
            provider_id=user_info.get("id"),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            avatar_url=user_data["avatar_url"]
        )
        
        # Create JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google authentication failed: {str(e)}")

@app.post("/auth/callback/facebook", response_model=Token)
async def facebook_callback(code: str, db: Session = Depends(get_db)):
    """Handle Facebook OAuth2 callback."""
    try:
        # Exchange code for token
        token = facebook_oauth.get_access_token(
            code=code,
            redirect_uri=os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:3000/auth/callback/facebook")
        )
        
        # Get user info from Facebook
        user_info = facebook_oauth.get_user_info(token=token)
        
        # Extract user data
        user_data = get_social_user_info("facebook", user_info)
        
        # Create or get user
        user = create_or_get_social_user(
            db=db,
            email=user_data["email"],
            provider="facebook",
            provider_id=user_info.get("id"),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            avatar_url=user_data["avatar_url"]
        )
        
        # Create JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Facebook authentication failed: {str(e)}")

@app.post("/auth/callback/apple", response_model=Token)
async def apple_callback(code: str, db: Session = Depends(get_db)):
    """Handle Apple OAuth2 callback."""
    try:
        # Exchange code for token
        token = apple_oauth.get_access_token(
            code=code,
            redirect_uri=os.getenv("APPLE_REDIRECT_URI", "http://localhost:3000/auth/callback/apple")
        )
        
        # Get user info from Apple
        user_info = apple_oauth.get_user_info(token=token)
        
        # Extract user data
        user_data = get_social_user_info("apple", user_info)
        
        # Create or get user
        user = create_or_get_social_user(
            db=db,
            email=user_data["email"],
            provider="apple",
            provider_id=user_info.get("sub"),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            avatar_url=user_data["avatar_url"]
        )
        
        # Create JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Apple authentication failed: {str(e)}")

@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    settings: str = Form(...),
    current_user: User = Depends(get_current_user)
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
async def ask_question_endpoint(
    request: dict,
    current_user: User = Depends(get_current_user)
):
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

@app.delete("/clear")
async def clear_database(current_user: User = Depends(get_current_user)):
    global manager
    
    try:
        import shutil
        
        # List of all possible database directories to clear
        directories_to_clear = [
            "chroma_db",
            "chroma_hr_db", 
            "chroma_kb_db",
            "backend/chroma_kb_db",
            "backend/chroma_hr_db",
            "src/chroma_hr_db",
            "src/chroma_kb_db"
        ]
        
        # If manager exists, add its persist directory and reset it
        if manager:
            directories_to_clear.append(manager.persist_directory)
            manager = None  # Reset the manager
        
        # Remove duplicates and clear all directories
        cleared_dirs = []
        for directory in set(directories_to_clear):
            if os.path.exists(directory):
                try:
                    shutil.rmtree(directory)
                    cleared_dirs.append(directory)
                    print(f"Cleared directory: {directory}")
                except Exception as e:
                    print(f"Failed to clear {directory}: {e}")
        
        if cleared_dirs:
            return {
                "message": f"Database cleared successfully from: {', '.join(cleared_dirs)}",
                "status": "success"
            }
        else:
            return {
                "message": "No database directories found to clear",
                "status": "info"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear database: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

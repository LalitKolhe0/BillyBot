from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for social auth users
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Social authentication fields
    provider = Column(String, nullable=True)  # 'google', 'facebook', 'apple', 'local'
    provider_id = Column(String, nullable=True)  # Social provider user ID
    avatar_url = Column(String, nullable=True)  # Profile picture URL
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

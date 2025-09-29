from sqlalchemy.orm import Session
from models import User
from auth import create_access_token, get_password_hash
from datetime import timedelta
import secrets
import string

def generate_username(email: str, provider: str) -> str:
    """Generate a unique username from email and provider."""
    base_username = email.split('@')[0]
    # Add random suffix to ensure uniqueness
    random_suffix = ''.join(secrets.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{base_username}_{provider}_{random_suffix}"

def create_or_get_social_user(
    db: Session, 
    email: str, 
    provider: str, 
    provider_id: str,
    first_name: str = None,
    last_name: str = None,
    avatar_url: str = None
) -> User:
    """Create or get existing social authentication user."""
    
    # Check if user exists with this email
    existing_user = db.query(User).filter(User.email == email).first()
    
    if existing_user:
        # If user exists but doesn't have this provider linked
        if existing_user.provider != provider:
            # Update existing user with social provider info
            existing_user.provider = provider
            existing_user.provider_id = provider_id
            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.avatar_url = avatar_url
            db.commit()
            db.refresh(existing_user)
        return existing_user
    
    # Create new user
    username = generate_username(email, provider)
    
    # Ensure username is unique
    counter = 1
    original_username = username
    while db.query(User).filter(User.username == username).first():
        username = f"{original_username}_{counter}"
        counter += 1
    
    new_user = User(
        email=email,
        username=username,
        provider=provider,
        provider_id=provider_id,
        first_name=first_name,
        last_name=last_name,
        avatar_url=avatar_url,
        hashed_password=None  # No password for social auth users
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_social_user_info(provider: str, user_info: dict) -> dict:
    """Extract user information from different OAuth providers."""
    if provider == "google":
        return {
            "email": user_info.get("email"),
            "first_name": user_info.get("given_name"),
            "last_name": user_info.get("family_name"),
            "avatar_url": user_info.get("picture")
        }
    elif provider == "facebook":
        return {
            "email": user_info.get("email"),
            "first_name": user_info.get("first_name"),
            "last_name": user_info.get("last_name"),
            "avatar_url": user_info.get("picture", {}).get("data", {}).get("url")
        }
    elif provider == "apple":
        return {
            "email": user_info.get("email"),
            "first_name": user_info.get("name", {}).get("firstName"),
            "last_name": user_info.get("name", {}).get("lastName"),
            "avatar_url": None  # Apple doesn't provide avatar
        }
    else:
        return {
            "email": user_info.get("email"),
            "first_name": user_info.get("first_name"),
            "last_name": user_info.get("last_name"),
            "avatar_url": user_info.get("avatar_url")
        }

import os
from authlib.integrations.starlette_client import GoogleOAuth2, FacebookOAuth2
from authlib.integrations.fastapi_oauth2 import AppleOAuth2

# OAuth2 Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback/google")

FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET")
FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:3000/auth/callback/facebook")

APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID")
APPLE_CLIENT_SECRET = os.getenv("APPLE_CLIENT_SECRET")
APPLE_REDIRECT_URI = os.getenv("APPLE_REDIRECT_URI", "http://localhost:3000/auth/callback/apple")

# OAuth2 Clients
google_oauth = GoogleOAuth2(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET
)

facebook_oauth = FacebookOAuth2(
    client_id=FACEBOOK_CLIENT_ID,
    client_secret=FACEBOOK_CLIENT_SECRET
)

apple_oauth = AppleOAuth2(
    client_id=APPLE_CLIENT_ID,
    client_secret=APPLE_CLIENT_SECRET
)

# OAuth2 Scopes
GOOGLE_SCOPES = ["openid", "email", "profile"]
FACEBOOK_SCOPES = ["email", "public_profile"]
APPLE_SCOPES = ["name", "email"]

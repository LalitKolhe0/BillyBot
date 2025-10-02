"""
OAuth configuration removed

This file previously defined authlib OAuth2 clients for Google, Facebook, and
Apple. Those providers were removed per project decision. Keep this file as a
placeholder in case a future re-introduction of social logins is desired.
"""

def not_available(*args, **kwargs):
    raise RuntimeError("Social authentication providers disabled")

google_oauth = not_available
facebook_oauth = not_available
apple_oauth = not_available

GOOGLE_SCOPES = []
FACEBOOK_SCOPES = []
APPLE_SCOPES = []

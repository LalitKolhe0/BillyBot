"""
OAuth social helpers removed

This module previously contained helpers to create or retrieve social-auth users
for Google/Facebook/Apple. Social logins were intentionally removed from the
project. If you decide to re-enable social auth later, restore the original
implementation or reintroduce provider-specific logic here.

The application now uses local email/password authentication + JWT tokens.
"""

def not_available(*args, **kwargs):
    raise RuntimeError("Social authentication is disabled in this build")

create_or_get_social_user = not_available
get_social_user_info = not_available

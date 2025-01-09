# middleware.py
from threading import local

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

_user = local()


class CurrentUserMiddleware:
    """
    Middleware to store the current user in thread-local storage.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Default to anonymous user
        _user.user = AnonymousUser()

        # Check for Authorization header with Bearer token
        auth_header = request.headers.get('Authorization', None)
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Decode the token to get user info
                access_token = AccessToken(token)
                # Assumes `user_id` is in the token payload
                user_id = access_token['user_id']

                # Fetch the user from the database
                User = get_user_model()
                user = User.objects.get(id=user_id)

                if not user.is_delete:
                    _user.user = user
            except Exception:
                # Invalid token or user not found
                pass

        # Add the current user to the request object for convenience
        request.current_user = _user.user

        response = self.get_response(request)
        return response


def get_current_user():
    """Get the current user stored in the thread-local variable"""
    return getattr(_user, 'user', AnonymousUser())

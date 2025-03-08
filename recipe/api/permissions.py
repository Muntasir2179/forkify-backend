from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from recipe.api.authentication import GuestJWTAuthentication

class HasValidToken(BasePermission):
    """
    Custom permission that checks if the user has a valid JWT guest token.
    """

    def has_permission(self, request, view):
        auth = GuestJWTAuthentication()

        try:
            user, token = auth.authenticate(request)

            if user is not None and token is not None:
                return True  # Valid token, grant access
        except Exception as e:
            raise AuthenticationFailed('Access credential is invalid or not provided!', code=status.HTTP_401_UNAUTHORIZED)

        return False  # No valid token found

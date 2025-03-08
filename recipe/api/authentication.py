from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from datetime import datetime, timezone

class GuestJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that validates JWT tokens for guest users.
    It allows authentication without requiring a `user_id`.
    """

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            return None  # No token found, authentication not attempted

        raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None  # No token found, authentication not attempted

        try:
            # Validate the token (AccessToken checks for expiry)
            validated_token = AccessToken(raw_token)
            
            validated_token.verify()  # 🚀 This explicitly checks expiration

            # Ensure the token has a guest_id
            if "guest_id" not in validated_token:
                raise AuthenticationFailed("Token is missing guest_id", code=status.HTTP_401_UNAUTHORIZED)

            # Check if the token has expired
            if validated_token["exp"] < datetime.now(timezone.utc).timestamp():
                raise AuthenticationFailed("Token has expired", code=status.HTTP_401_UNAUTHORIZED)

            # Return a dummy user object (since we are not using Django users)
            return ({"guest_id": validated_token["guest_id"]}, validated_token)

        except Exception as e:
            raise AuthenticationFailed("Invalid or expired token", code=status.HTTP_401_UNAUTHORIZED)

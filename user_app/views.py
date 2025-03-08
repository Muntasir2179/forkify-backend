from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from datetime import datetime, timedelta
import uuid

# Create your views here.

@api_view(["GET",])
def register_user(request):
    return Response(data={'data': 'Request Successful'})


class GenerateTokenForGuestView(APIView):
    permission_classes = [AllowAny]  # Allows anyone to generate a token

    def post(self, request):
        # Generate a unique guest ID (UUID)
        guest_id = str(uuid.uuid4())  # Random unique identifier for guest users
        
        # Create a custom token payload
        token = AccessToken()
        token["guest_id"] = guest_id  # Include guest ID in the token payload
        token.set_exp(from_time=datetime.now(), lifetime=timedelta(hours=1))  # Fixed expiration time

        return Response({
            "access_token": str(token),
            "expires_in": '1 hour',  # 1 hour in seconds
            "guest_id": guest_id  # Return guest ID for reference
        })

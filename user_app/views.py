from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from datetime import datetime, timedelta
import uuid

# Create your views here.

class GenerateTokenForGuestView(APIView):
    permission_classes = [AllowAny]  # Allows anyone to generate a token

    def post(self, request):
        guest_id = str(uuid.uuid4())  # Generate a unique guest ID
        
        token = AccessToken()
        token["guest_id"] = guest_id  # Attach guest ID to the token

        # Set token expiration (1 hour from now)
        expiry_time = datetime.utcnow() + timedelta(hours=1)
        token.set_exp(from_time=datetime.utcnow(), lifetime=timedelta(hours=1))

        return Response({
            "access_token": str(token),
            "expires_at": expiry_time,
            "guest_id": guest_id
        })

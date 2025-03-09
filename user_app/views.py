from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user_app.models import AccessKey
from user_app.serializers import AccessKeySerializer

# Create your views here.

class GenerateTokenForGuestView(APIView):  
    def post(self, request):
        access_key = AccessKey.objects.create()
        serializer = AccessKeySerializer(access_key)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

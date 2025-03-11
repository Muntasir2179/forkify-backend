from rest_framework import serializers
from user_app.models import AccessKey

class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        exclude = ('id', )

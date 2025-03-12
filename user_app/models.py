from django.db import models
import uuid

# Create your models here.

def generate_access_key():
    return str(uuid.uuid4())  # Generates a 36-character unique key


class AccessKey(models.Model):
    access_key = models.CharField(max_length=36, unique=True, default=generate_access_key)
    
    def __str__(self):
        return self.access_key

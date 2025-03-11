from django.urls import path
from user_app import views

urlpatterns = [
    path('generate-token/', view=views.GenerateTokenForGuestView.as_view(), name='generate-token'),
]

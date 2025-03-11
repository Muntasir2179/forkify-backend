from django.urls import path, include
from recipe import views as app_views

urlpatterns = [
    path('', view=app_views.Index.as_view(), name='index'),
    path('forkify/', include('recipe.api.urls')),
]

from django.urls import path
from recipe.api import views as api_views

urlpatterns = [
    path('recipes/', view=api_views.AddRetrieveSearchRecipe.as_view(), name='all-recipe'),
    path('recipes/<str:id>/', view=api_views.SingleRecipe.as_view(), name='single-recipe'),
]
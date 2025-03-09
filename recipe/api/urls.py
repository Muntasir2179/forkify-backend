from django.urls import path
from recipe.api import views

urlpatterns = [
    path('recipes/', view=views.AllRecipe.as_view(), name='all-recipe'),
    path('recipes/<str:id>/', view=views.SingleRecipe.as_view(), name='single-recipe'),
]
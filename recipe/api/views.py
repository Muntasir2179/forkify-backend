from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from recipe.models import Recipes
from recipe.api.serializers import RecipeSerializer
from recipe.api.helpers import format_ingredients
from recipe.api.permissions import HasValidToken
from recipe.api.authentication import GuestJWTAuthentication
# Create your views here.

class AllRecipe(APIView):
    '''
    Usage:
        1. Handles all recipe request but excludes user added recipes
        2. Handles specific search recipe request
    '''
    def get(self, request):
        try:
            query = request.query_params.get('search')
            if query == None:
                err_message = 'No recipes found'  # setting up error message for all recipe case if it needs
                recipes = Recipes.objects.all()
            else:
                err_message = 'No such recipes found! Try something else!'  # setting up recipe for search case if it needs
                recipes = Recipes.objects.filter(title__contains=query)
        except Recipes.DoesNotExist:
            return Response({'error': err_message}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecipeSerializer(recipes, many=True)
        data = []
        for item in serializer.data:
            if item['key'] == None:  # only keep those recipes which are not created by any user (user created recipe will contain key)
                item.pop('key')
                item.pop('created_at')
                item['ingredients'] = format_ingredients(item['ingredients'])
                data.append(item)
        
        return Response(data=data, status=status.HTTP_200_OK)


class SingleRecipe(APIView):
    def get(self, request, id):
        try:
            recipe = Recipes.objects.get(id=id)
            serializer = RecipeSerializer(recipe)
            data = serializer.data
            data['ingredients'] = format_ingredients(serializer.data['ingredients'])
            return Response(data=data, status=status.HTTP_200_OK)
        except Recipes.DoesNotExist:
            return Response(data={'error': 'No recipe found!'}, status=status.HTTP_404_NOT_FOUND)


class AllRecipeIncludeUser(APIView):
    """
    This view is protected by the HasValidToken permission.
    Only users with a valid JWT guest token can access it.
    """
    authentication_classes = [GuestJWTAuthentication]  # Use custom authentication
    permission_classes = [HasValidToken]  # Apply the custom permission

    def get(self, request):
        token = request.auth  # we can access the token from request.auth
        
        try:
            recipes = Recipes.objects.filter(key=None)
            user_recipes = Recipes.objects.filter(key=token)  # fetching recipes create by user
        except Recipes.DoesNotExist:
            return Response({'response': 'No recipes found!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecipeSerializer(recipes, many=True)
        user_recipes_serializer = RecipeSerializer(user_recipes, many=True)

        return Response(data=serializer.data + user_recipes_serializer.data, status=status.HTTP_200_OK)

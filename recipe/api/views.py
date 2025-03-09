from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from recipe.models import Recipes
from recipe.api.serializers import RecipeSerializer
from recipe.api.helpers import format_recipe
from recipe.api.permissions import HasValidToken
from recipe.api.authentication import GuestJWTAuthentication
# Create your views here.

class AllRecipe(APIView):
    '''
    Usage:
        1. Handles search recipes request
        2. Handles user recipes request using key
    '''
    def get(self, request):
        combined_recipes = []
        query = request.query_params.get('search')
        token = request.query_params.get('key')
        
        if query or token:
            # if search query is passed
            if query:
                recipes = Recipes.objects.filter(title__contains=query)
                serializer = RecipeSerializer(recipes, many=True)
                combined_recipes += serializer.data
            
            # if key is passed
            if token:
                user_recipes = Recipes.objects.filter(key=token)
                user_recipes_serializer = RecipeSerializer(user_recipes, many=True)
                combined_recipes += user_recipes_serializer.data
            
            data = {
                'status': 'success',
                'result': 0,
                'data': {
                    'recipes': []
                }
            }
            
            for item in combined_recipes:
                if item['key'] != None and item['key'] != '':
                    data['data']['recipes'].append(format_recipe(item, single=False, user=True))
                else:
                    data['data']['recipes'].append(format_recipe(item, single=False, user=False))
                data['result'] += 1
            
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "failed",
                             "message": "Key and Search query not provided!"}, status=status.HTTP_400_BAD_REQUEST)


class SingleRecipe(APIView):
    def get(self, request, id):
        try:
            recipe = Recipes.objects.get(id=id)
            serializer = RecipeSerializer(recipe)
            result = serializer.data
            data = {
                'status': 'success',
                'data': {
                    'recipe': format_recipe(result, single=True, user=result['key'] != None and result['key'] != '')
                },
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Recipes.DoesNotExist:
            return Response(data={
                    'status': 'fail',
                    'message': 'Invalid ID'
                }, status=status.HTTP_400_BAD_REQUEST)


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

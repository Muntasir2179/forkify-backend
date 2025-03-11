from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from recipe.models import Recipes
from recipe.api.serializers import RecipeSerializer
from recipe.api.helpers import format_recipe
from user_app.models import AccessKey
# Create your views here.

class AddRetrieveSearchRecipe(APIView):
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
                recipes = Recipes.objects.filter(title__contains=query, key=None)
                serializer = RecipeSerializer(recipes, many=True)
                combined_recipes += serializer.data

            # if key is passed
            if token:
                user_recipes = Recipes.objects.filter(key=token)
                user_recipes_serializer = RecipeSerializer(user_recipes, many=True)
                combined_recipes += user_recipes_serializer.data
            
            data = {
                'status': 'success',
                'results': 0,
                'data': {
                    'recipes': []
                }
            }
            
            for item in combined_recipes:
                if item['key'] != None and item['key'] != '':
                    data['data']['recipes'].append(format_recipe(item, single=False, user=True))
                else:
                    data['data']['recipes'].append(format_recipe(item, single=False, user=False))
                data['results'] += 1
            
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "failed",
                             "message": "Key and Search query not provided!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request):
        token = request.query_params.get('key')
        data = request.data
        
        try:
            is_token = AccessKey.objects.get(access_key=token)  # checking if the token exists or not
        except Exception:
            raise AuthenticationFailed(
                {
                    'status': 'fail',
                    'message': 'You are not authorized to access this endpoint! Check your access key!'
                },
                code=status.HTTP_401_UNAUTHORIZED
            )
        
        data['key'] = token  # add the access token to the data to store in recipe
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(
                {
                    'status': 'Success',
                    'data': {
                        'recipe': RecipeSerializer(recipe).data
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'status': 'fail',
                'message': serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


class SingleRecipe(APIView):
    def get(self, request, id):
        try:
            token = request.query_params.get('key')
            recipe = Recipes.objects.get(id=id)
            
            result = None
            if recipe.key != None and recipe.key != '' and recipe.key == token:  # recipe got a key and it is as same as user sent token
                serializer = RecipeSerializer(recipe)
                result = serializer.data
            elif recipe.key == None or recipe.key == '':   # recipe got no key, it is a public recipe
                serializer = RecipeSerializer(recipe)
                result = serializer.data
            elif recipe.key != None and recipe.key != '' and recipe.key != token:  # recipe got a key and it is not as same as user sent token
                # result will be none
                pass
            
            data = {
                'status': 'success',
                'data': {
                    'recipe': format_recipe(result, single=True, user=result['key'] != None and result['key'] != '') if result else {}
                },
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Recipes.DoesNotExist:
            return Response(data={
                    'status': 'fail',
                    'message': 'Invalid id or key'
                }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            token = request.query_params.get('key')
            recipe = Recipes.objects.get(id=id)
            data = None
            
            if recipe.key != None and recipe.key != '' and recipe.key == token:  # recipe got a key and it is as same as user sent token
                # have to delete the recipe
                serializer = RecipeSerializer(recipe)
                data = serializer.data
                recipe.delete()  # delete the recipe
            else:
                # this user is not authorized to delete this recipe
                return Response(data={
                    'status': 'fail',
                    'message': 'You are not authorized to delete this recipe'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response(data={
                    'status': 'success',
                    'data': {
                        'recipe': format_recipe(data, single=True, user=True)
                    }
                }, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={
                    'status': 'fail',
                    'message': 'Invalid id or key'
                }, status=status.HTTP_400_BAD_REQUEST)

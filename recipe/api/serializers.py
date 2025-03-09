from rest_framework import serializers
from recipe.models import Unit, Ingredient, Recipes

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['unit_name']  # Excluding 'id'

class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.SlugRelatedField(
        queryset=Unit.objects.all(),
        slug_field='unit_name',
        allow_null=True,
        required=False
    )
    
    class Meta:
        model = Ingredient
        fields = ['quantity', 'unit', 'description']  # Excluding 'id'

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    
    class Meta:
        model = Recipes
        fields = [
            'id', 'key', 'created_at', 'cooking_time', 'image_url', 'publisher', 'servings',
            'source_url', 'title', 'ingredients'
        ]
        read_only_fields = ['id']  # Ensuring id is generated automatically

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        
        for ingredient_data in ingredients_data:
            unit_name = ingredient_data.pop('unit', None)
            unit = None
            if unit_name:
                unit, created = Unit.objects.get_or_create(unit_name=unit_name)
            ingredient = Ingredient.objects.create(unit=unit, **ingredient_data)
            recipe.ingredients.add(ingredient)
        
        return recipe

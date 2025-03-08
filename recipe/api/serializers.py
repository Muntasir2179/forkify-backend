from rest_framework import serializers
from recipe.models import Unit, Recipes, Ingredient


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        exclude = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    class Meta:
        model = Ingredient
        exclude = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Recipes
        fields = '__all__'

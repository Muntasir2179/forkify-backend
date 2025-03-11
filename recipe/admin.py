from django.contrib import admin
from recipe.models import Recipes, Ingredient, Unit

# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'cooking_time')
    list_display_links = ('title',)
    list_filter = ('title', 'publisher', 'cooking_time')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('description',)
    list_display_links = ('description',)


admin.site.register(Recipes, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Unit)

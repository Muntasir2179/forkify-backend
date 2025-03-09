
def format_ingredients(ingredients: list):
    new_ingredients = []
    for item in ingredients:
        new_ingredients.append({
            'unit': item['unit']['unit_name'] if item['unit'] != None else None,
            'quantity': item['quantity'],
            'description': item['description']
        })
    return new_ingredients


def format_recipe(recipe: dict, single:bool, user:bool):
    new_recipe = {}
    if single:
        excludes = ['key', 'created_at']
    else:
        excludes = ['key', 'created_at', 'cooking_time', 'servings', 'source_url', 'ingredients']
    
    if user:
        excludes.remove('key')
    
    for key, value in recipe.items():
        if key not in excludes:
            if key == 'ingredients':
                new_recipe[key] = format_ingredients(value)
            else:
                new_recipe[key] = value
    
    return new_recipe

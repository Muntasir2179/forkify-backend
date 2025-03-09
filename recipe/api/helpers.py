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
            new_recipe[key] = value
    
    return new_recipe

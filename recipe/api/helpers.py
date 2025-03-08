
def format_ingredients(ingredients: list):
    new_ingredients = []
    for item in ingredients:
        new_ingredients.append({
            'unit': item['unit']['unit_name'] if item['unit'] != None else None,
            'quantity': item['quantity'],
            'description': item['description']
        })
    return new_ingredients

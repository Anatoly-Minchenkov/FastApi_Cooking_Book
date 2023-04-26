from db.models import UniqueIngredient

def check_unique_ingredients(session, ingredients):
    unique_ingredients = [uniq_ingredient.name for uniq_ingredient in session.query(UniqueIngredient).all()]
    for i in ingredients:
        if i.name not in unique_ingredients:
            session.add(UniqueIngredient(name=i.name))
            session.commit()
    return True
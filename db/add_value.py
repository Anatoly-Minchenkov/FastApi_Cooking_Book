import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models import Ingredient, Recipe, Step


# engine = sa.create_engine('postgresql://bcraft:password@localhost:5432/bcraft')
# #
# Session = sessionmaker(bind=engine)
# session = Session()
# #
# recept_ingredients = []
# for ingredient_name, quantity in [("Пирожок", 32), ("Сахар", 40), ("Кругетсы", 21)]:
#     ingredient = session.query(Ingredient).filter_by(name=ingredient_name).first()
#     if ingredient is None:
#         ingredient = Ingredient(name=ingredient_name)
#         session.add(ingredient)
#     recept_ingredients.append(RecipeIngredient(ingredient=ingredient, quantity=quantity))

#ingredients = [RecipeIngredient(ingredient=Ingredient(name=ingredient_name), quantity=quantity)] #пояснялка для ingredients снизу.


# new_recipe = Recipe(name="Пирожок с кругетсами", description="Вкусно", steps=[Step(step_description='шаг1', step_time=33)], ingredients=recept_ingredients)
# print(new_recipe)
# session.add(new_recipe)
# session.commit()


#####пример заполнения со старыми таблицами, без ingridients
# {
#     "name": "Картофель в мундире",
#     "description": "Жарить не надо",
#     "steps": [
#         {
#             "step_description": "сварить",
#             "step_time": 30
#         },
#         {
#             "step_description": "пожарить",
#             "step_time": 30
#         }
#     ],
#     "ingredients": [
#         {
#             "ingredient": {
#                 "name": "картошка"
#
#             },
#             "quantity": 2
#         }
#     ]
# }



# pie_ingredients = []
# for ingredient_name, quantity in [("Яблоки", 1), ("Мука", 300), ("Сахар", 150), ("Масло", 100)]:
#     ingredient = session.query(Ingredient).filter_by(name=ingredient_name).first()
#     if ingredient is None:
#         ingredient = Ingredient(name=ingredient_name)
#         session.add(ingredient)
#     pie_ingredients.append(RecipeIngredient(ingredient=ingredient, quantity=quantity))
#
# salad_ingredients = []
# for ingredient_name, quantity in [("Помидоры", 2), ("Огурцы", 2), ("Лук", 1), ("Масло", 50), ("Укроп", 20)]:
#     ingredient = session.query(Ingredient).filter_by(name=ingredient_name).first()
#     if ingredient is None:
#         ingredient = Ingredient(name=ingredient_name)
#         session.add(ingredient)
#     salad_ingredients.append(RecipeIngredient(ingredient=ingredient, quantity=quantity))
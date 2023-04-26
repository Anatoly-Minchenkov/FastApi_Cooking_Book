import copy

from db.models import *
import schemas

import uvicorn
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker, joinedload
from sqlalchemy import create_engine

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "postgresql://bcraft:password@localhost:5432/bcraft"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Получение списка всех рецептов
@app.get("/recipes/", response_model=List[schemas.Recipe])
def read_recipes(session: Session = Depends(get_db)):
    ''''''
    recipe_db = session.query(Recipe).all()
    return recipe_db

# Получение рецепта по id
@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, session: Session = Depends(get_db)):
    recipe_db = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe_db is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_db

# Добавление рецепта в бд
@app.post("/recipes/add_recipe")
def create_recipe(recipe: schemas.Recipe, session: Session = Depends(get_db)):
    steps = [Step(**step.dict()) for step in recipe.steps]
    ingredients = [Ingredient(**ingredient.dict()) for ingredient in recipe.ingredients]
    recipe_db = Recipe(name=recipe.name, description=recipe.description, ingredients=ingredients, steps=steps)
    session.add(recipe_db)
    session.commit()
    session.refresh(recipe_db)

    ####заполнение уникальными ингридиентами таблицу
    unique_ingredients = [uniq_ingredient.name for uniq_ingredient in session.query(UniqueIngredient).all()]
    for i in ingredients:
        if i.name not in unique_ingredients:
            session.add(UniqueIngredient(name=i.name))
            session.commit()

    return recipe

# Обновление информации о рецепте из бд
@app.put("/recipes/update/{recipe_id}")
def update_recipe(recipe: schemas.Recipe, recipe_id: int, session: Session = Depends(get_db)):
    recipe_db = session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe_db:
        return {"error": "Recipe not found"}
    # Удаление старых ингредиентов
    session.query(Ingredient).filter_by(recipe_id=recipe_id).delete()
    # Добавление новых ингредиентов
    new_ingredients = [Ingredient(name=ingredient.name, quantity=ingredient.quantity, recipe_id=recipe_id)
                       for ingredient in recipe.ingredients]
    session.add_all(new_ingredients)
    # Удаление старых шагов
    session.query(Step).filter_by(recipe_id=recipe_id).delete()
    # Добавление новых шагов
    new_steps = [Step(step_description=step.step_description, step_time=step.step_time, recipe_id=recipe_id)
                 for step in recipe.steps]
    session.add_all(new_steps)
    # Обновление информации о рецепте
    recipe_db.name = recipe.name
    recipe_db.description = recipe.description
    session.commit()
    session.refresh(recipe_db)
    return {"new_recipe": recipe}

# Удаление рецепта из бд
@app.delete("/recipes/delete/{recipe_id}")
def delete_recipe(recipe_id: int, session: Session = Depends(get_db)):
    recipe_db = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe_db is None:
        session.rollback()
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.delete(recipe_db)
    session.commit()
    return {"message": f"Recipe with id {recipe_id} has been deleted."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

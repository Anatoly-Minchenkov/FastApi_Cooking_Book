from db.models import *
from db import schemas
import spec_functions
import uvicorn
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
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
def get_all_recipes(session: Session = Depends(get_db)):
    recipe_db = session.query(Recipe).all()
    return recipe_db


# Получение рецепта по id
@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe_by_id(recipe_id: int, session: Session = Depends(get_db)):
    recipe_db = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe_db is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_db


# Добавление рецепта в бд
@app.post("/recipes/add_recipe")
def add_new_recipe(recipe: schemas.RecipeUpdate, session: Session = Depends(get_db)):
    steps = [Step(**step.dict()) for step in recipe.steps]
    ingredients = [Ingredient(**ingredient.dict()) for ingredient in recipe.ingredients]
    recipe_db = Recipe(name=recipe.name, description=recipe.description, ingredients=ingredients, steps=steps)
    session.add(recipe_db)
    session.commit()
    session.refresh(recipe_db)

    spec_functions.check_unique_ingredients(session, ingredients)
    return recipe


# Обновление информации о рецепте из бд
@app.put("/recipes/update/{recipe_id}")
def update_recipe_by_id(recipe: schemas.RecipeUpdate, recipe_id: int, session: Session = Depends(get_db)):
    recipe_db = session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe_db:
        return {"error": "Recipe not found"}
    # Удаление старых ингредиентов
    session.query(Ingredient).filter_by(recipe_id=recipe_id).delete()
    # Добавление новых ингредиентов, если есть
    if recipe.ingredients:
        new_ingredients = [Ingredient(name=ingredient.name, quantity=ingredient.quantity, recipe_id=recipe_id)
                        for ingredient in recipe.ingredients]
        session.add_all(new_ingredients)
        # Проверка на новые уникальные ингредиенты
        spec_functions.check_unique_ingredients(session, new_ingredients)

    # Удаление старых шагов
    session.query(Step).filter_by(recipe_id=recipe_id).delete()
    # Добавление новых шагов, если есть
    if recipe.steps:
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
def delete_recipe_by_id(recipe_id: int, session: Session = Depends(get_db)):
    recipe_db = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe_db is None:
        session.rollback()
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.delete(recipe_db)
    session.commit()
    return {"message": f"Recipe with id {recipe_id} has been deleted."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

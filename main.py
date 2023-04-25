import json
from typing import List

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db.models import *
import schemas
from crud import cru

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


@app.get("/recipes/", response_model=List[schemas.Recipe])
def read_recipes(session: Session = Depends(get_db)):
    recipes = session.query(Recipe).all()
    return recipes


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def read_recipe(recipe_id: int, session: Session = Depends(get_db)):
    recipe = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


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

@app.put("/recipes/update/{recipe_id}")
def update_recipe(recipe: schemas.Recipe, recipe_id: int, session: Session = Depends(get_db)):
    pass

@app.delete("/recipes/delete/{recipe_id}")
def delete_recipe(recipe_id: int,  session: Session = Depends(get_db)):
    recipe = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe is None:
        session.rollback()
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.delete(recipe)
    session.commit()
    return {"message": f"Recipe with id {recipe_id} has been deleted."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

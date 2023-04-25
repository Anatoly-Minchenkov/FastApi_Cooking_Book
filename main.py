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
def create_recipe(recipe:schemas.Recipe, session: Session = Depends(get_db)):

    # ingredients = [RecipeIngredient(quantity=ri.quantity, ingredient=Ingredient(name=ri.ingredient.name)) for ri in recipe.ingredients]


    steps = [Step(**step.dict()) for step in recipe.steps]
    recipe_db = Recipe(name=recipe.name, description=recipe.description, steps=steps)
    session.add(recipe_db)
    session.commit()
    session.refresh(recipe_db)

    return recipe

    # ingredients = []
    # for ri in recipe.ingredients:
    #     ingredient = Ingredient(name=ri.ingredient.name)
    #     recipe_ingredient = RecipeIngredient(quantity=ri.quantity, ingredient=ingredient)
    #     ingredients.append(recipe_ingredient[0])

    # db_recipe = Recipe(name=recipe.name, description=recipe.description, steps=steps)
    # session.add(db_recipe)

    return 'ok'


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
from typing import List, Optional
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str

    # id: int
    class Config:
        orm_mode = True


class RecipeIngredient(BaseModel):
    ingredient: Ingredient
    quantity: Optional[float] = 0.0

    # id: int
    # recipe_id: int
    # ingredient_id: int
    class Config:
        orm_mode = True


class Step(BaseModel):
    step_description: str
    step_time: int

    # id: int
    # recipe_id: int
    # recipe: 'Recipe'
    class Config:
        orm_mode = True


class Recipe(BaseModel):
    id: Optional[int] = '0'
    name: str
    description: str
    ingredients: List[RecipeIngredient]
    steps: List[Step]

    class Config:
        orm_mode = True




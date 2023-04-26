from typing import List, Optional
from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = 0.0

    # recipe_id: int
    # recipe: 'Recipe'
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
    id: int
    name: str
    description: str
    ingredients: List[Ingredient]
    steps: List[Step]

    class Config:
        orm_mode = True

class RecipeUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = []
    steps: Optional[List[Step]] = []

    class Config:
        orm_mode = True


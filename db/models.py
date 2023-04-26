from sqlalchemy import Column, String, Integer, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://bcraft:password@localhost:5432/bcraft')
Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete")
    steps = relationship("Step", back_populates="recipe", cascade="all, delete")


class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(String, default='По вкусу')
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="ingredients")


class Step(Base):
    __tablename__ = 'step'
    id = Column(Integer, primary_key=True, autoincrement=True)
    step_description = Column(String)
    step_time = Column(Integer)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship('Recipe', back_populates='steps')


class UniqueIngredient(Base):
    __tablename__ = 'unique_ingredient'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)



Base.metadata.create_all(engine)

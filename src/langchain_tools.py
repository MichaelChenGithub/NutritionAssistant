from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchRun
from assistant_tool_recipe import * 
from assistant_tool_nutrition import * 

class RecipeInput(BaseModel):
    query: str = Field(description="food name")

class NutritionInput(BaseModel):
    query: str = Field(description="serving size and food name")

class RestaurantInput(BaseModel):
    query: str = Field(description="general food name")

def get_tools():
    recipe_tool = StructuredTool.from_function(
        func=get_recipe,
        name="get_recipe",
        description="Fetch recipes and cusine nutrition",
        args_schema=RecipeInput
    )
    nutrition_tool = StructuredTool.from_function(
        func=get_nutrition_with_nlp,
        name="get_nutrition_with_nlp",
        description="Fetch Food nutrition",
        args_schema=NutritionInput
    )
    restaurant_food_tool = StructuredTool.from_function(
        func=find_restaurant_food,
        name="find_restaurant_food",
        description="Find restaurant food options",
        args_schema=RestaurantInput
    )
    tools = [DuckDuckGoSearchRun(), recipe_tool, nutrition_tool, restaurant_food_tool]
    return tools
from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import GoogleSearchAPIWrapper
from assistant_tool_recipe import * 
from assistant_tool_nutrition import * 



class RecipeInput(BaseModel):
    query: str = Field(description="food name")

class NutritionInput(BaseModel):
    query: str = Field(description="serving size and food name")

class RestaurantInput(BaseModel):
    query: str = Field(description="general food name")

class GoogleSearch(BaseModel):
    query: str = Field(description="search query")

def get_tools():
    recipe_tool = StructuredTool.from_function(
        func=search_meal_by_name,
        name="search_meal_by_name",
        description="Fetch recipes and cusine ingredient and steps",
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
    google_search_tool = StructuredTool.from_function(
        func=GoogleSearchAPIWrapper().run,
        name="google_search",
        description="Search Google for related results",
        args_schema=GoogleSearch
    )
    tools = [recipe_tool, nutrition_tool, restaurant_food_tool, google_search_tool]
    return tools
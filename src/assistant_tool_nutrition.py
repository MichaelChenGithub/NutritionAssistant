import os
import requests

def get_nutrition_with_nlp(query):
    """
    Retrieves nutritional information for foods using natural language processing from the Nutritionix API.

    Parameters:
        query (str): The user's natural language query describing the food for which they want to obtain nutritional information.

    Returns:
        list: A list of dictionaries containing filtered nutritional information. Each dictionary represents the nutritional information for one food item.

    Exceptions:
        Returns an error message string if the request fails or if an exception occurs during the API call.
    """
    headers = {
        "Content-Type": "application/json",
        "x-app-id": os.getenv("NUTRITIONNIX_APP_ID"),
        "x-app-key": os.getenv("NUTRITIONNIX_APP_KEY")
    }
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    payload = {
        "query": query
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # if error happened, raise the error status
        saved_response = []
        # only keep important nutrition info to minimize the token
        for food in response.json()["foods"]:
            keys_to_remove = set(['full_nutrients', 'nix_brand_name', 'nix_brand_id', 'nix_item_name', 'nix_item_id', 'upc', 'consumed_at', 'source', 'ndb_no', 'lat', 'lng', 'meal_type', 'photo', 'sub_recipe', 'class_code', 'brick_code', 'tag_id'])
            saved_food_info = {key: value for key, value in food.items() if key not in keys_to_remove}
            saved_response.append(saved_food_info)
        return saved_response
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
def find_restaurant_food(query):
    """
    Searches for branded foods in the Nutritionix API based on the search query.

    Parameters:
        query (str): The search query used to find foods, which can include food names, brands, etc.

    Returns:
        list: A list of dictionaries containing the search results. Each dictionary includes key information such as the food name and brand name.

    Exceptions:
        Returns a dictionary with an error message if the request fails or if an exception occurs during the API call.
    """
    headers = {
        "Content-Type": "application/json",
        "x-app-id": os.getenv("NUTRITIONNIX_APP_ID"),
        "x-app-key": os.getenv("NUTRITIONNIX_APP_KEY")
    }
    url = f"https://trackapi.nutritionix.com/v2/search/instant/?query={query}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # if error happened, raise the error status
        branded_food = response.json()["branded"]
        saved_response = []
        # only keep important nutrition info to minimize the token
        for food in branded_food:
            keys_to_save = set(['food_name', 'brand_name_item_name', 'brand_name'])
            saved_food_info = {key: value for key, value in food.items() if key in keys_to_save}
            saved_response.append(saved_food_info)
        return saved_response
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
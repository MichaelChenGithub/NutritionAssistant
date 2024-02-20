import os
import requests


def get_nutrition_with_nlp(query):
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
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
def find_restaurant_food(query):
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
        return branded_food
    except requests.exceptions.RequestException as e:
        return {"error": f"Error: {e}"}
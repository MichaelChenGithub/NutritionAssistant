import requests

def search_meal_by_name(query):
    headers = {
        "Content-Type": "application/json",
        "API-key" : "1"
    }

    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # if error happened, raise the error status
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
import requests

def search_meal_by_name(query):
    """
    Searches for meal information by name using TheMealDB API.

    Parameters:
        query (str): The name of the meal to search for. This can be a full name or a partial name, as the API supports searching with partial matches.

    Returns:
        dict: A dictionary containing the API's response. This includes an array of meals that match the search query, with each meal containing details such as its name, category, area, instructions, and ingredients.

    Exceptions:
        Returns an error message string if the request encounters an error or if an exception occurs during the API call. This could be due to various reasons such as network issues, invalid API keys, or errors from TheMealDB API.

    Notes:
        The function uses a GET request to retrieve data from TheMealDB API based on the search query provided. The 'API-key' in the headers is a placeholder and should be replaced with a valid API key if required by TheMealDB API.
    """
    headers = {
        "Content-Type": "application/json",
        "API-key" : "1"
    }

    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # if error happened, raise the error status
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
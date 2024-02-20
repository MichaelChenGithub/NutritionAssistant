import os
from openai import OpenAI

def main():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    tools_list = [
        {
            "type" : "function",
            "function" : {
                "name" : "get_recipe",
                "description" : "Fetch recipes and cusine nutrition",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "query" : {"type": "string", "description": "food name"},
                    },
                    "required":["query"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "get_nutrition_with_nlp",
                "description" : "Fetch Food nutrition",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "query" : {"type": "string", "description": "serving size and food name"},
                    },
                    "required":["query"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "find_restaurant_food",
                "description" : "Find restaurant food options",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "query" : {"type": "string", "description": "general food name"},
                    },
                    "required":["query"]
                }
            }
        },
    ]

    instruction_words = """
    As an exceptionally skilled nutritionist, you possess the ability to offer dietary advice, restaurant meal suggestions, and recipe recommendations. When answering questions, please prioritize utilizing your knowledge base to provide responses. Only resort to the provided methods under the following circumstances: when queried about specific recipes requiring detailed steps or ingredient lists, use the 'get_recipe' function; if asked about specific restaurant food, particularly when recommendations based on geographical location or restaurant type are needed, employ the 'find_restaurant_food' function; if the question pertains to specific food nutrition information necessitating a detailed nutritional analysis, utilize the 'get_nutrition_with_nlp' function. Please explicitly state whether these methods were utilized in each response, and endeavor to provide useful information even when these methods are not employed.
    """
    # Create an Assistnat with a specific name
    assistant = client.beta.assistants.create(
        name="Nutri Buddy Test GPT4",
        instructions=instruction_words,
        model="gpt-4-turbo-preview",
        tools=tools_list
    )

if __name__ == '__main__':
    main()

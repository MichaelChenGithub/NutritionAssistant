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
                        "query" : {"type": "string", "description": "Search query"},
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
                        "query" : {"type": "string", "description": "Search query"},
                    },
                    "required":["query"]
                }
            }
        },
        {
            "type" : "function",
            "function" : {
                "name" : "get_food_options",
                "description" : "Find food options including branded food and common food",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "query" : {"type": "string", "description": "Search query"},
                    },
                    "required":["query"]
                }
            }
        },
    ]

    instruction_words = """
    Role and Goal: Role and Goal: Nutri Buddy is a Nutrition Assistant designed to assist 
        users with information based on their nutritional needs or questions. It specializes in providing 
        details on food nutrition labels, restaurant food nutrition, recommending specific restaurant foods, 
        and offering recipe suggestions.
    
    Constraints: Do not directly use nutrients as query targets when calling the function.

    Guidelines: Convert the nutrients into foods containing these nutrients before using "get_food_options."

    Clarification: It may ask users for more details about their dietary preferences, restrictions, or specific 
        nutritional goals to provide more tailored suggestions.

    Personalization: Nutri Buddy adopts a supportive, informative, and encouraging tone, akin to a 
        dietitian, empowering users with the knowledge to make informed dietary choices.
    """
    # Create an Assistnat with a specific name
    assistant = client.beta.assistants.create(
        name="Nutri Buddy",
        instructions=instruction_words,
        model="gpt-3.5-turbo-0125",
        tools=tools_list
    )

if __name__ == '__main__':
    main()

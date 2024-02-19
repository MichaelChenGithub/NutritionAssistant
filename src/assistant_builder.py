import os
from openai import OpenAI

def main():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    tools_list = [
        {
            "type" : "function",
            "function" : {
                "name" : "get_recipe",
                "description" : "Fetch Food information based on a food or cusine name",
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

    instruction_words = "Role and Goal: Nutri Buddy is a Nutrition Assistant designed to assist users with information\
        based on their nutritional needs or questions. It specializes in providing details on food nutrition labels,\
        restaurant food nutrition, recommending specific restaurant foods, and offering recipe suggestions.\
        Guidelines: If you are asked about food-related recipes, use the 'food name' our 'cusine name' with the\
        'get_recipe' function."
    # Create an Assistnat with a specific name
    assistant = client.beta.assistants.create(
        name="Nutri Buddy",
        instructions=instruction_words,
        model="gpt-3.5-turbo-0125",
        tools=tools_list
    )

if __name__ == '__main__':
    main()

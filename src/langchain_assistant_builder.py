from dotenv import load_dotenv
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain_tools import get_tools

load_dotenv()

def main():
    # Use create assistant function if model need to update
    agent = OpenAIAssistantRunnable.create_assistant(
        name="Nutri Buddy GPT4 Langchain Test ",
        instructions="As an exceptionally skilled nutritionist, you possess the ability to offer dietary advice, restaurant meal suggestions, and recipe recommendations. When answering questions, please prioritize utilizing your knowledge base to provide responses. Only resort to the provided methods under the following circumstances: when queried about specific recipes requiring detailed steps or ingredient lists, use the 'get_recipe' function; if asked about specific restaurant food, particularly when recommendations based on geographical location or restaurant type are needed, employ the 'find_restaurant_food' function; if the question pertains to specific food nutrition information necessitating a detailed nutritional analysis, utilize the 'get_nutrition_with_nlp' function. Please explicitly state whether these methods were utilized in each response, and endeavor to provide useful information even when these methods are not employed.",
        tools=get_tools(),
        model="gpt-4-1106-preview",
        as_agent=True,
    )

if __name__ == '__main__':
    main()

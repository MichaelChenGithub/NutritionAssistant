from openai import OpenAI
from sk import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

intstructions_string = "ShenNutritionGPT can provide dietary recommendations \
based on your nutritional needs through your food preferences. \
In addition to recommending basic ingredients, it can also suggest \
suitable options for dining out and prepare recipes for you, \
making it much easier for you to control your diet."

assistant = client.beta.assistants.create(
    name="ShenNutritionGPT",
    description="Food Nutrition GPT for Diet Recommendation",
    instructions=intstructions_string,
    model="gpt-3.5-turbo-0125"
)

# create thread (i.e. object that handles conversation between user and assistant)
thread = client.beta.threads.create()

# add a user message to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Great content, thank you!"
)

# send message to assistant to generate a response
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
import streamlit as st
# from langchain.agents import AgentExecutor
from langchain.tools import DuckDuckGoSearchRun
from assistant_tool_recipe import * 
from assistant_tool_nutrition import * 
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
load_dotenv()
from langchain_core.agents import AgentFinish


def execute_agent(agent, tools, input):
    tool_map = {tool.name: tool for tool in tools}
    response = agent.invoke(input)
    while not isinstance(response, AgentFinish):
        tool_outputs = []
        for action in response:
            tool_output = tool_map[action.tool].invoke(action.tool_input)
            print(action.tool, action.tool_input, tool_output, end="\n\n")
            tool_outputs.append(
                {"output": tool_output, "tool_call_id": action.tool_call_id}
            )
        response = agent.invoke(
            {
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": action.thread_id,
            }
        )

    return response

class RecipeInput(BaseModel):
    query: str = Field(description="food name")

recipe_tool = StructuredTool.from_function(
    func=get_recipe,
    name="get_recipe",
    description="Fetch recipes and cusine nutrition",
    args_schema=RecipeInput
)

class NutritionInput(BaseModel):
    query: str = Field(description="serving size and food name")

nutrition_tool = StructuredTool.from_function(
    func=get_nutrition_with_nlp,
    name="get_nutrition_with_nlp",
    description="Fetch Food nutrition",
    args_schema=NutritionInput
)

class RestaurantInput(BaseModel):
    query: str = Field(description="general food name")

restaurant_food_tool = StructuredTool.from_function(
    func=find_restaurant_food,
    name="find_restaurant_food",
    description="Find restaurant food options",
    args_schema=RestaurantInput
)

tools = [DuckDuckGoSearchRun(), recipe_tool, nutrition_tool, restaurant_food_tool]
assistant_id = "asst_kjXxune3YNpmyZ6dMbij9W1m"

llm = OpenAI(temperature=0, streaming=True, openai_api_key=os.getenv("OPENAI_API_KEY"))

agent = OpenAIAssistantRunnable(assistant_id=assistant_id, as_agent=True)

# agent_executor = AgentExecutor(agent=agent, tools=tools)
# if 'client' not in st.session_state:
#         # Initialize the client
#         st.session_state.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         # Step 1: Retrive the assistant
#         st.session_state.assistant = st.session_state.client.beta.assistants.retrieve("asst_ZTAFYXG4fdP2t57Wr5Nga85v")

#         # Step 2: Create a Thread
#         st.session_state.thread = st.session_state.client.beta.threads.create()

#     user_query = st.text_input("Enter your query:", "I need 10g protein. Do you have any food suggestions?")
#     intstructions_string = """
#         For basic dietary advice or information queries, the expectation is that the Assistant primarily relies on its extensive knowledge base to provide answers. Specific functions or methods should be reserved for cases where detailed recipes, restaurant recommendations, or comprehensive nutritional 
#         analyses are explicitly requested. Do not return pictures.
#     """



# try: "what are the names of the kids of the 44th president of america"
# try: "top 3 largest shareholders of nvidia"
if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st.write("🧠 thinking...")
        st_callback = StreamlitCallbackHandler(st.container())
        if 'thread_id' not in locals():
            response = execute_agent(agent, tools, {"content": "What's 10 - 4 raised to the 2.7"})
            print(response.return_values["output"])
            thread_id = response["thread_id"]
        else:
            next_response = execute_agent(
                agent,
                tools,
                {"content": "now add 17.241", "thread_id": thread_id},
            )
        st.write(response["output"])


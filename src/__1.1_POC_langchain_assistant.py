import os
from dotenv import load_dotenv
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
from langchain_tools import get_tools
import streamlit as st

# load_dotenv()

def main():
    assistant_id = "asst_kjXxune3YNpmyZ6dMbij9W1m"

    ## Use create assistant function if model need to update
    # agent = OpenAIAssistantRunnable.create_assistant(
    #     name="Nutri Buddy GPT4 Langchain Test ",
    #     instructions="As an exceptionally skilled nutritionist, you possess the ability to offer dietary advice, restaurant meal suggestions, and recipe recommendations. When answering questions, please prioritize utilizing your knowledge base to provide responses. Only resort to the provided methods under the following circumstances: when queried about specific recipes requiring detailed steps or ingredient lists, use the 'get_recipe' function; if asked about specific restaurant food, particularly when recommendations based on geographical location or restaurant type are needed, employ the 'find_restaurant_food' function; if the question pertains to specific food nutrition information necessitating a detailed nutritional analysis, utilize the 'get_nutrition_with_nlp' function. Please explicitly state whether these methods were utilized in each response, and endeavor to provide useful information even when these methods are not employed.",
    #     tools=tools,
    #     model="gpt-4-1106-preview",
    #     as_agent=True,
    # )
    agent = OpenAIAssistantRunnable(assistant_id=assistant_id, as_agent=True)
    agent_executor = AgentExecutor(agent=agent, tools=get_tools())

    if 'messages' not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.empty()
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        response = None
        with st.chat_message("assistant"):
            st.write("🧠 thinking...")
            if 'thread_id' not in st.session_state:
                response = agent_executor.invoke({"content": prompt})
                st.session_state.thread_id = response["thread_id"]
            else:
                response = agent_executor.invoke({"content": prompt, "thread_id": st.session_state.thread_id})
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
            st.write(response["output"])
            

if __name__ == '__main__':
    main()

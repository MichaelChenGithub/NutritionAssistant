import os
from dotenv import load_dotenv
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
from langchain_tools import get_tools
import streamlit as st

load_dotenv()

def main():
    st.set_page_config(page_title="Nourish X", page_icon="🥚")
    st.title("🥚 Nourish X")
    # OPENAI_APIKEY = os.environ.get("OPEN_AI_KEY")
    openai_api_key_input = st.sidebar.text_input("OpenAI API Key", type="password")

    if 'messages' not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "I'm a nutritionist here to help you live healthier!"}
        ]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.empty()
        st.chat_message("user").write(prompt)
        
        if not openai_api_key_input:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        
        openai_api_key = openai_api_key_input

        try:
            assistant_id = "asst_kjXxune3YNpmyZ6dMbij9W1m"
            agent = OpenAIAssistantRunnable(assistant_id=assistant_id, openai_api_key=openai_api_key, as_agent=True)
            agent_executor = AgentExecutor(agent=agent, tools=get_tools())
            with st.chat_message("assistant"):
                st.write("🧠 thinking...")
                if 'thread_id' not in st.session_state:
                    response = agent_executor.invoke({"content": prompt})
                    st.session_state.thread_id = response["thread_id"]
                else:
                    response = agent_executor.invoke({"content": prompt, "thread_id": st.session_state.thread_id})
                st.session_state.messages.append({"role": "assistant", "content": response["output"]})
                st.write(response["output"])
        except:
            st.info("Your OpenAI API KEY is unavailable or not correct.")
            st.stop()

if __name__ == '__main__':
    main()

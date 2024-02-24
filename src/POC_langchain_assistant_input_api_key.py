import os
import asyncio
from dotenv import load_dotenv
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
# from langchain_community.callbacks import get_openai_callback
# from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_tools import get_tools
import streamlit as st
from openai import OpenAI

load_dotenv()

def main():
    st.set_page_config(page_title="Nourish", page_icon="🥚")
    st.title("🥚 Nourish")
    OPENAI_APIKEY = os.environ.get("OPEN_AI_KEY")
    TESTING_PASSWORD = os.environ.get("TESTING_PASSWORD")
    password = st.sidebar.text_input("Password", type="password")

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
        
        if not password:
            st.info("Please enter the password to continue.")
            st.stop()
        if password == TESTING_PASSWORD:
            assistant_id = "asst_F3YhhK6JzfaQPlekDgCGTK9X"
            agent = OpenAIAssistantRunnable(client= OpenAI(api_key=OPENAI_APIKEY), assistant_id=assistant_id, as_agent=True, verbose=True)
            agent_executor = AgentExecutor(agent=agent, tools=get_tools(), verbose=True)
            with st.chat_message("assistant"):
                st.write("🧠 thinking...")
                if 'thread_id' not in st.session_state:
                    response = agent_executor.invoke({"content": prompt})
                    
                    st.session_state.thread_id = response["thread_id"]
                else:
                    response = agent_executor.invoke({"content": prompt, "thread_id": st.session_state.thread_id})
                st.session_state.messages.append({"role": "assistant", "content": response["output"]})
                st.write(response["output"])

        else:
            # st.info("Your password is not correct.")
            # st.stop()
            st.error("Your password is wrong.")
    


if __name__ == '__main__':
    main()

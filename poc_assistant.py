from openai import OpenAI
import time
import streamlit as st
from sk import OPENAI_API_KEY

def main():

    if 'client' not in st.session_state:
        # Initialize the client
        st.session_state.client = OpenAI(api_key=OPENAI_API_KEY)

        # Step 1: Retrive the assistant
        st.session_state.assistant = st.session_state.client.beta.assistants.retrieve("asst_Z4knqwOe9olvisDtzZGP0Fxo")

        # Step 2: Create a Thread
        st.session_state.thread = st.session_state.client.beta.threads.create()

    user_query = st.text_input("Enter your query:", "I need 10g protein. Do you have any food suggestions?")
    intstructions_string = """
        ShenNutritionGPT provides dietary recommendations \
        based on your nutritional needs through your food preferences. \
        In addition to recommending basic ingredients, it can also suggest \
        suitable options for dining out and prepare recipes for you, \
        making it much easier for you to control your diet.
    """

    if st.button('Submit'):
        # Step 3: Add a Message to a Thread
        message = st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=user_query
        )

        # Step 4: Run the Assistant
        run = st.session_state.client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
            instructions= intstructions_string
        )

        while True:
            # Wait for 5 seconds
            time.sleep(5)

            # Retrieve the run status
            run_status = st.session_state.client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=run.id
            )

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = st.session_state.client.beta.threads.messages.list(
                    thread_id=st.session_state.thread.id
                )

                # Loop through messages and print content based on role
                for msg in messages.data[::-1]:
                    role = msg.role
                    content = msg.content[0].text.value
                    st.write(f"{role.capitalize()}: {content}")
                break
            else:
                st.write("Waiting for the Assistant to process...")
                time.sleep(3)

if __name__ == "__main__":
    main()
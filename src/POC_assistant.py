from assistant_tool_recipe import * 
from assistant_tool_nutrition import * 
from openai import OpenAI
import time
import json
import streamlit as st
import os

def main():
    if 'client' not in st.session_state:
        # Initialize the client
        st.session_state.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Step 1: Retrive the assistant
        st.session_state.assistant = st.session_state.client.beta.assistants.retrieve("asst_gB2efcBXZVufEh6e8IoXRn33")

        # Step 2: Create a Thread
        st.session_state.thread = st.session_state.client.beta.threads.create()

    user_query = st.text_input("Enter your query:", "I need 10g protein. Do you have any food suggestions?")
    intstructions_string = """
        As a nutrition assistant, please provide the best nutritional advice based on your knowledge and collected data.
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
                thread_id= st.session_state.thread.id,
                run_id=run.id
            )
            print(run_status.model_dump_json(indent=4))

            # Define a dispatch table
            function_dispatch_table = {
                "get_recipe": get_recipe,
                "get_nutrition_with_nlp": get_nutrition_with_nlp,
                "get_food_options": get_food_options
            }

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = st.session_state.client.beta.threads.messages.list(
                    thread_id= st.session_state.thread.id
                )

                # Loop through messages and print content based on role
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    st.write(f"{role.capitalize()}: {content}")
                break
            elif run_status.status == 'requires_action':
                print("Requires action")
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                print(required_actions)
                tools_output = []

                for action in required_actions["tool_calls"]:
                    func_name = action["function"]["name"]
                    arguments = json.loads(action["function"]["arguments"])

                    func = function_dispatch_table.get(func_name)
                    if func:
                        result = func(**arguments)
                        # Ensure the output is a JSON string
                        output = json.dumps(result) if not isinstance(result, str) else result
                        tools_output.append({
                            "tool_call_id": action["id"],
                            "output": output
                        })
                    else:
                        print(f"Function {func_name} not found")

                # Submit the tool outputs to Assistant API
                st.session_state.client.beta.threads.runs.submit_tool_outputs(
                    thread_id= st.session_state.thread.id,
                    run_id=run.id,
                    tool_outputs=tools_output
                )
            else:
                st.write("Waiting for the Assistant to process...")
                time.sleep(5)

if __name__ == "__main__":
    main()
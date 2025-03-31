# This script is designed to run a local LLM to answer questions about the American Community Survey (ACS) B and C tables.
# Gareth Minson-Efimov
# 2025-03-13

# Packages
from gpt4all import GPT4All
import random
import json
import streamlit as st
import time

# set seed
random.seed(16)

def load_text_file(filepath):
    """Loads the contents of a text file into a string."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

file_path = "public_data/03_processed/b_c_tables.json"  # Replace with your file path
file_content = load_text_file(file_path)

table_items = list(file_content.items())
random.shuffle(table_items)
sample_data = dict(table_items[:5]) 

print("Tables: ", sample_data.keys())  # Print the keys of the sample data for debugging

# Convert the sample dictionary to a string
sample_data = json.dumps(sample_data)

if file_content is None:
    print(f"Error: Could not load file from {file_path}")
    sys.exit(1)  # Exit with an error code

system_prompt = f"""
You are an expert policy analyst working for the U.S. Census Bureau. Your role is to assist users in understanding and interpreting data from the American Community Survey (ACS), specifically focusing on the B (Base) and C (Collapsed) tables.

**Data File (ACS Table Information):**

{sample_data}

**Instructions for Using the Data File:**

1.  **Parsing:** Treat the text file above as a string representation of JSON data. You must be able to parse this string to extract the table information.
2.  **Table Lookup:** When a user asks about a specific table (by ID or title), search the parsed data for the corresponding table entry.
3.  **Variable Retrieval:** If a user requests the variables for a table, extract the "variables" list from the corresponding table entry.
4.  **Table Type Identification:** Determine if a table is a B table or a C table using the "table_type" field.
5.  **C Table Relationships:** For C tables, use the "derived_from" field to identify the corresponding B table.
6.  **Response Generation:** When responding to user queries, include relevant information from the parsed data, such as:
    * Table ID
    * Table Title
    * Table Type (B or C)
    * List of Variables
    * Relationship to B table (for C tables)
7.  **Data Limitations:** If the user asks about a table or variable that is not in the provided data file, respond that you do not have that information.
8.  **B Table and C Table Definitions:** You must still utilize the base definitions of the B and C tables provided in the previous prompts to give context to the data.
9.  **Clear Communication:** Present information in a clear and concise manner.
10. **Offline Functionality:** Remember that you are operating in an offline environment. You must rely on the information provided in this prompt and data file.
11. **Avoid Hallucinations:** When you do not have the data to answer a question, state that you do not have the data, do not make something up.

**Example User Interactions:**

* User: "What variables are in table B01001?"
* User: "Is there data on income in the provided tables?"

**Your goal is to accurately parse the provided text file and use the extracted data to answer user questions about ACS B and C tables.** 
"""

# Initialize GPT4All with the model name. Replace with actual model path if needed.
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", verbose=False)

def generate_prompt(user_input):
    prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
    return prompt

# App Dev
st.write("Census Bureau Chatbot")

st.caption("This might not work")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
with model.chat_session():
    try:
        while True:
            prompt = st.chat_input("Enter your question (or type 'exit' to quit): ")
            print(prompt)
            quiet_prompt = generate_prompt(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = model.generate(quiet_prompt, max_tokens=1024, temp=0.5,)
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
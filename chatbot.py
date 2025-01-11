import streamlit as st

def start_chatbot():
    st.title("Traveladvisor")

if 'messages' not in st.session_state:
    st.session_state.message = []

#Dispaly Historical message
for messages in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

#Prompt input template to dispaly the prompts
prompt = st.chat_input("Ask something here")

#User clicks enter
if prompt:
    #Display the prompt
    st.chat_message('user').markdown(prompt)
    #Store the prompt
    st.session_state.messages.append({'role':'user', 'content':prompt})
# Function call to start the chatbot
start_chatbot()

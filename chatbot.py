import streamlit as st
import openai
import pandas as pd
from llama_index.llms.openai import OpenAI
from llama_index import VectorStoreIndex, Document, Settings

# Streamlit page configuration
st.set_page_config(
    page_title="Chat with CSV Data, powered by LlamaIndex",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

openai.api_key = st.secrets.openai_key
st.title("Chat with Your CSV Data, powered by LlamaIndex 💬🦙")
st.info(
    "Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)",
    icon="📃",
)

# Initialize chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about the uploaded CSV data!",
        }
    ]

@st.cache_resource(show_spinner=False)
def load_csv_data(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert the DataFrame into documents for LlamaIndex
    documents = [
        Document(text=row.to_string(index=False)) for _, row in df.iterrows()
    ]
    # Set up the LLM
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        system_prompt="""You are an expert at analyzing CSV datasets. 
        Your job is to answer technical questions based on the data. 
        Keep your answers factual and concise.""",
    )
    # Create an index from the documents
    index = VectorStoreIndex.from_documents(documents)
    return index


# File uploader in Streamlit
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    index = load_csv_data(uploaded_file)
    if "chat_engine" not in st.session_state.keys():
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=True, streaming=True
        )

    if prompt := st.chat_input("Ask a question about the CSV data"):  # User input
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Display message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Generate assistant's response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            response_stream = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response_stream.response_gen)
            message = {"role": "assistant", "content": response_stream.response}
            st.session_state.messages.append(message)
else:
    st.warning("Please upload a CSV file to get started.")

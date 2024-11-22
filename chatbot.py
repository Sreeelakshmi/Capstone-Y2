import streamlit as st

def start_chatbot():
    st.subheader("Travel Chatbot")

    # Initialize session state for chatbot memory
    if "history" not in st.session_state:
        st.session_state.history = []

    # Input box for user query
    query = st.text_input("Ask me anything about travel!")
    
    if query:
        # Generate a basic response
        response = f"Here's a suggestion for '{query}'."
        # Add conversation to session state history
        st.session_state.history.append(f"**User:** {query}")
        st.session_state.history.append(f"**Bot:** {response}")
    
    # Display chat history
    for message in st.session_state.history:
        st.write(message)

    # Add sidebar for travel filters
    st.sidebar.header("Customize Your Trip")
    location = st.sidebar.selectbox("Choose a location", ["Paris", "Tokyo", "New York"])
    budget = st.sidebar.slider("Budget ($)", 500, 10000, 2500)
    st.sidebar.write(f"Searching for trips to {location} under ${budget}...")

    # Show example multimedia for selected locations
    if location == "Paris":
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e6/Eiffel_Tower_(72_names).jpg", caption="Eiffel Tower, Paris")
    elif location == "Tokyo":
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/0d/Shinjuku_by_Night.jpg", caption="Shinjuku, Tokyo")
    elif location == "New York":
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/47/New_york_times_square-terabass.jpg", caption="Times Square, New York")

    # Feedback mechanism
    feedback = st.radio("Was this response helpful?", ["Yes", "No"])
    if feedback == "No":
        improvement_suggestion = st.text_area("What can we improve?")
        if improvement_suggestion:
            st.write("Thank you for your feedback!")

# Function call to start the chatbot
start_chatbot()

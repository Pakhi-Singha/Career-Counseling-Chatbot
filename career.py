import streamlit as st
import ollama

# Title of the app
st.title("Career Guidance AI Chatbot")

# Sidebar for user preferences
with st.sidebar:
    st.header("Career Guidance Settings")
    user_name = st.text_input("Your Name", "User")
    user_education = st.selectbox("Your Education Level", ["High School", "Undergraduate", "Graduate", "Postgraduate"])
    user_experience = st.slider("Years of Work Experience", 0, 30, 0)
    user_interests = st.text_area("What are your career interests?", "AI, Data Science, Engineering, Marketing")

# System message for context
system_message = f"""
You are a career counselor AI. Provide helpful career advice based on the user's education, experience, and interests.
Be clear and encouraging.
User Details:
- Name: {user_name}
- Education: {user_education}
- Experience: {user_experience} years
- Interests: {user_interests}
"""

# User input
user_input = st.text_input("Ask a career question:")

if user_input:
    # Query Llama model via Ollama
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
    )
    
    # Display response
    st.write("### AI Response:")
    st.write(response["message"])  # Fixed key reference

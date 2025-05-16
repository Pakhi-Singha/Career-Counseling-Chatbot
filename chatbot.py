import streamlit as st
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

# Load the embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="career_guidance")

# Load knowledge base (optional)
def load_knowledge():
    try:
        with open("career_knowledge.txt", "r") as f:
            documents = f.readlines()
            for i, doc in enumerate(documents):
                embedding = embedder.encode(doc).tolist()
                collection.add(documents=[doc], ids=[str(i)], embeddings=[embedding])
    except FileNotFoundError:
        st.warning("No knowledge base found. Continuing without it.")

load_knowledge()

# Streamlit UI
st.title("Career Guidance AI Chatbot")

with st.sidebar:
    st.header("Career Guidance Settings")
    user_name = st.text_input("Your Name", "User")
    user_education = st.selectbox("Your Education Level", ["High School", "Undergraduate", "Graduate", "Postgraduate"])
    user_experience = st.slider("Years of Work Experience", 0, 30, 0)
    user_interests = st.text_area("What are your career interests?", "AI, Data Science, Engineering, Marketing")

# System message
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
    # Embed query and find relevant documents
    query_embedding = embedder.encode(user_input).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    retrieved_docs = "\n".join(results["documents"][0]) if results["documents"] else ""

    # Add context from vector DB
    full_prompt = f"{system_message}\n\nRelevant Info:\n{retrieved_docs}\n\nQuestion: {user_input}"

    # Ask LLM
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": full_prompt}
        ]
    )

    st.write("### AI Response:")
    st.write(response["message"])

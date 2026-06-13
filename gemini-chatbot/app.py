import os
import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI College Assistant", page_icon="🎓", layout="centered")
st.title("🎓 AI Engineering Assistant")
st.caption("A smart chatbot powered by Google Gemini API to help with tech, coding, and mini-projects.")

# 2. API Key Configuration
# Securely fetches the API key from system environment variables
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing Gemini API Key. Please configure GEMINI_API_KEY in your environment/hosting platform.")
    st.stop()

# Configure the Gemini SDK
genai.configure(api_key=api_key)

# 3. Initialize Gemini Chat Model & Session State Memory
if "chat_session" not in st.session_state:
    # System instruction sets the bot's behavior/topic context
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="You are a helpful, brilliant academic assistant for B.Tech engineering students. Answer technical queries concisely and clearly."
    )
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Display Existing Chat History (Streamlit handles UI rendering)
for message in st.session_state.chat_session.history:
    # Map Gemini's internal roles to Streamlit's visual components
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. User Input Action Loop
if user_prompt := st.chat_input("Ask me anything about engineering..."):
    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response from Gemini API with a clean loading spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat_session.send_message(user_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
import streamlit as st
import speech_recognition as sr
import time
from retrievalFaiss import user_input

# Simulate a function that generates a response with a delay
def generate_response(user_message):
    response = user_input(user_message)
    time.sleep(2)  # Simulating a delay for response generation
    return f" {response}"

# Function to capture voice input
def capture_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
        try:
            st.info("Recognizing...")
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Sorry, I did not understand the audio.")
        except sr.RequestError:
            st.error("Could not request results; check your internet connection.")
        return None

# Function to display chat interface
def chat_interface():

    # Add option to switch between text and voice input
    input_mode = st.radio("Choose input method:", ("Text", "Voice"))
    prompt = None

    if input_mode == "Text":
        prompt = st.chat_input("Type your message here")
    else:
        if st.button("Click to Speak"):
            prompt = capture_voice_input()

    for chat in st.session_state.Rag:
        if chat["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"You: {chat['content']}")
        else:
            with st.chat_message("assistant"):
                st.markdown(f"Assistant: {chat['content']}")

    if prompt is not None:
        # Add user message to chat history
        st.session_state.Rag.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f"You: {prompt}")

        # Display loading message
        loading_message_placeholder = st.empty()
        loading_message_placeholder.markdown("Loading...")

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # key = st.secrets["gemini_key"]
            response = generate_response(prompt)
            st.markdown(f"Assistant: {response}")

        # Clear loading message and display response
        loading_message_placeholder.empty()
        st.session_state.Rag.append({"role": "assistant", "content": response})

# Main application
if __name__ == "__main__":
    # Initialize session state for API key and messages
    if "Rag" not in st.session_state:
        st.session_state.Rag = []

    # Main app layout
    st.set_page_config(page_title="Multilingual AI Assistant", layout="wide")

    st.title("AI Chat")
    chat_interface()
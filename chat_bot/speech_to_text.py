import speech_recognition as sr
import streamlit as st
from chat_bot.text_to_speech import speak_response
from chat_bot.logger import logger

# Function to capture voice input using the default microphone
def capture_voice_input():
    recognizer = sr.Recognizer()
    user_question = None
    try:
        with sr.Microphone() as source:
            st.write("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            logger.info("Audio data captured for speech recognition.")
        
        user_question = recognizer.recognize_google(audio)
        logger.info(f"Voice Input Recognized: {user_question}")
        st.write(f"You said: {user_question}")
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand the audio.")
        logger.warning("Could not understand the audio.")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        logger.error(f"RequestError in Google Speech Recognition: {str(e)}")
    except Exception as e:
        logger.error(f"Error during speech recognition: {str(e)}")

    return user_question

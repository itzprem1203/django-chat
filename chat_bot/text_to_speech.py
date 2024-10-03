import pyttsx3
import threading
from chat_bot.logger import logger

# Lock for handling the speech engine execution
speech_lock = threading.Lock()
is_speaking = False

# Function to speak text response
def speak_response(text):
    global is_speaking

    def run_speech():
        global is_speaking
        try:
            with speech_lock:
                is_speaking = True
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                logger.info(f"Spoken response: {text}")
                is_speaking = False
        except Exception as e:
            logger.error(f"Error in speech synthesis: {str(e)}")
            is_speaking = False

    if not is_speaking:
        speech_thread = threading.Thread(target=run_speech)
        speech_thread.start()
    else:
        logger.warning("Attempted to start speaking while another speech is active.")

import streamlit as st
from chat_bot.pdf_processing import get_pdf_text, get_text_chunks
from chat_bot.text_to_speech import speak_response
from chat_bot.speech_to_text import capture_voice_input
from chat_bot.embedding_store import get_vector_store
from chat_bot.conversational_chain import get_pdf_conversational_chain, get_general_conversational_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chat_bot.logger import logger  # Import the logger

import os

# Set the Google application credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\itzpr.DESKTOP-EUQC32B\Desktop\django-chat\gen-lang-client-0848981992-22fdd0980d68.json"

def user_input(user_question):
    logger.info(f"Query: {user_question}")  # Log user question
    
    if user_question.lower() == "what is your name":
        response_text = "My name is Prem's AI Assistant, a helpful assistant for you!"
        logger.info(f"Reply: {response_text}")  # Log response
        speak_response(response_text)
        return response_text

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)

        if docs:
            chain = get_pdf_conversational_chain()
            response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        else:
            raise ValueError("No context found in the PDFs")
    except Exception as e:
        logger.error(f"Error during PDF search: {e}")  # Log the error
        chain = get_general_conversational_chain()
        response = chain({"question": user_question}, return_only_outputs=True)

    response_text = response["output_text"]
    logger.info(f"Reply: {response_text}")  # Log response
    speak_response(response_text)
    
    return response_text

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with YouAre, the Helpful Assistant 💁")

    user_question = st.text_input("Ask a Question from the PDFs or General Knowledge")
    reply = ""

    if st.button("Ask via Voice"):
        st.write("You have selected the voice assistant button to ask a query.")
        voice_input = capture_voice_input()  # Capture voice input
        
        if voice_input:
            reply = user_input(voice_input)  # Process the voice input
            if reply:
                st.write("Reply: ", reply)
                speak_response(reply)  # Speak the response
        else:
            st.write("Please ask one more time to recognize your voice.")

    if user_question:
        reply = user_input(user_question)
        if reply:
            st.write("Reply: ", reply)
            speak_response(reply)  # Speak the response

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True, type=["pdf"])
        
        if st.button("Submit & Process"):
            with st.spinner("Processing PDFs..."):
                raw_text = ""
                for pdf in pdf_docs:
                    raw_text += get_pdf_text(pdf)

                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)

                st.success("Processed PDFs and created embeddings successfully.")

if __name__ == '__main__':
    main()

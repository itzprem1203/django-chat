from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chat_bot.logger import logger

# Function to create a vector store using FAISS
def get_vector_store(text_chunks):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        logger.info("Vector store created successfully.")

        num_vectors = vector_store.index.ntotal
        logger.info(f"Total number of texts in the vector store: {num_vectors}")

        vector_store.save_local("faiss_index")
        logger.info("Vector store saved locally at 'faiss_index'.")
    except Exception as e:
        logger.error(f"Error in creating vector store: {str(e)}")
    return vector_store

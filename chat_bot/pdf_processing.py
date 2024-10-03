import logging
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chat_bot.logger import logger

# Function to extract text from PDF using PdfReader
def get_pdf_text(pdf_file):
    text = ""
    try:
        reader = PdfReader(pdf_file)
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        logger.info(f"Extracted text from {pdf_file}. Total pages: {len(reader.pages)}")
    except Exception as e:
        logger.error(f"Failed to extract text from {pdf_file}: {str(e)}")
    return text

# Function to split text into chunks
def get_text_chunks(text):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        logger.info(f"Number of text chunks created: {len(chunks)}")
    except Exception as e:
        logger.error(f"Error while splitting text into chunks: {str(e)}")
        chunks = []
    return chunks

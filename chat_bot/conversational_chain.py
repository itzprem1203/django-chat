from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from chat_bot.logger import logger

# Function to get the conversational chain for PDF-related queries
def get_pdf_conversational_chain():
    try:
        prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details.
        Context:\n {context}?\n Question: \n{question}\n Answer:
        """
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        logger.info("PDF conversational chain created successfully.")
    except Exception as e:
        logger.error(f"Error in creating PDF conversational chain: {str(e)}")
    return chain

# Function to get the conversational chain for general questions
def get_general_conversational_chain():
    try:
        prompt_template = """
        My name is YouAre, a very helpful assistant. Feel free to ask anything.
        Question: {question}\n Answer:
        """
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        logger.info("General conversational chain created successfully.")
    except Exception as e:
        logger.error(f"Error in creating general conversational chain: {str(e)}")
    return chain

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
key = os.getenv("GEMINI_API_KEY")


def get_conversational_chain():
    global key

    # Define a prompt template for asking questions based on a given context
    prompt_template = """
    As a legal chat bot and you are a legal professional specializing in Indian Penal Code queries, your primary objective is to provide accurate and concise information based on the user's questions. Do not generate your own questions and answers. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from posing additional questions. The aim is to deliver professional, precise, and contextually relevant information pertaining to the Indian Penal Code.
    You have to give me IPC sections which can be against the culprit\n\n
    LawBook:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """

    # Initialize a ChatGoogleGenerativeAI model for conversational AI
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=key)

    # Create a prompt template with input variables "context" and "question"
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Load a question-answering chain with the specified model and prompt
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    global key
    print(key)
    # Create embeddings for the user question using a Google Generative AI model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=key
    )

    # Load a FAISS vector database from a local file
    new_db = FAISS.load_local("ipc", embeddings, allow_dangerous_deserialization=True)

    # Perform similarity search in the vector database based on the user question
    docs = new_db.similarity_search(user_question, k=3)

    # Obtain a conversational question-answering chain
    chain = get_conversational_chain()

    # Use the conversational chain to get a response based on the user question and retrieved documents
    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )

    # Print the response to the console
    return response["output_text"]

import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

groq_api_key = os.getenv('GROQ_API_KEY')
openai_api_key = os.getenv('OPEN_API_KEY')
hfk = os.getenv('HFK')

# Set up Streamlit UI
st.set_page_config(page_title='Apple Device ChatBot', page_icon=':apple:', layout='wide')
st.title('Welcome to the Apple Device ChatBot')

# Add a sidebar with instructions
st.sidebar.header('Instructions')
st.sidebar.write("Use this chatbot to get answers about Apple devices. Simply type your query in the text input box.")
st.sidebar.write("You can adjust the creativity of the responses using the 'Adjust Temperature' slider.")

# Load the CSV data
csv_file = 'apple_data_csv.csv'
loader = CSVLoader(file_path=csv_file)
data = loader.load()

# Cache the vector store
@st.cache_resource
def create_vector_store():
    embed = HuggingFaceEmbeddings()
    vector_store = FAISS.from_documents(data, embed)
    return vector_store

vector_store = create_vector_store()

# Create a retriever from the cached vector store
@st.cache_resource
def get_retriever():
    return vector_store.as_retriever()

retriever = get_retriever()

# Define the prompt template
prompt_template = """
    Here are some examples:
    Example 1:
    <context>
    To take a screenshot on an iPhone, press and hold the Side button and the Volume Up button simultaneously. The screen will flash briefly, and a thumbnail of the screenshot will appear in the bottom-left corner of the screen. Tap the thumbnail to view or edit the screenshot.
    </context>
    Question: How do I take a screenshot on an iPhone?
    Answer: To take a screenshot on an iPhone, press and hold the Side button and the Volume Up button simultaneously. The screen will flash briefly, and a thumbnail of the screenshot will appear in the bottom-left corner of the screen. Tap the thumbnail to view or edit the screenshot.
    If you don’t know the answer, simply write "I don’t know."
    You have some flexibility; you can frame your answer creatively, but it should be contextual.
    Answer the following question based on the context provided:
    <context>
    {context}
    </context>
    Question: {input}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

# Set up user input and temperature slider
st.sidebar.subheader('Chat Settings')
temperature = st.sidebar.slider('Adjust Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.01)

# Instantiate the LLM (using Groq's model)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it", temperature=temperature)

# If user input is provided, process it
user_input = st.text_input('Ask me queries related to Apple devices', placeholder='Type your question here...')
if user_input:
    # Create chains
    docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, docs_chain)
    result = retrieval_chain.invoke({"input": user_input})
    
    # Display the output in Streamlit
    st.markdown(f"**Answer:** {result['answer']}")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ by Aditya")

# # Add an image or logo (optional)
# st.image("path_to_logo.png", width=100)


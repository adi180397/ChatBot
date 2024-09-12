# Apple Device ChatBot
This project is a chatbot application designed to assist users with questions related to Apple devices. It is built using Streamlit for the user interface and Langchain for managing document retrieval and language model interactions. The chatbot is powered by a Groq model and uses FAISS for efficient vector search.<br>

## Project Structure
app.py: The main script that powers the Streamlit-based web app. It handles user inputs, interacts with the chatbot model, and displays the results.<br>
apple_data_csv.csv: The CSV file containing a collection of Q&A data related to Apple devices. This dataset is used to provide relevant answers to user queries.<br>
.env: A file for storing sensitive environment variables such as API keys.<br>
## Features
Streamlit UI: The app provides an intuitive interface with a text input box for user queries and sliders for adjusting the chatbot's response temperature (creativity).<br>
FAISS for Document Retrieval: FAISS is used to index and retrieve relevant documents from the CSV dataset, which are then used to generate context-based responses.<br>
Groq Model: The chatbot is powered by the Groq API's language model, which provides high-quality, human-like responses based on the input query and document context.<br>
Document Embeddings: HuggingFace embeddings are used to convert the documents into vector representations for FAISS indexing.<br>
Customizable Responses: Users can adjust the chatbot's response creativity via a temperature slider.
![image](https://github.com/user-attachments/assets/5af85129-b431-4071-87f7-474881216a21)



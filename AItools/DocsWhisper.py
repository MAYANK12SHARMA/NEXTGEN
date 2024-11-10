import os
import requests
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from AItools.htmlTemplates import css, bot_template, user_template

# Load environment variables
load_dotenv()

# Function to extract text from PDF files
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to get embeddings from Azure OpenAI API
def get_embeddings_from_azure(text_chunks, api_key):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # Update endpoint to match your Azure configuration
    endpoint = "https://api-code-gen.openai.azure.com/openai/deployments/text-embedding-ada-002-2/embeddings?api-version=2023-05-15"

    embeddings = []
    for chunk in text_chunks:
        data = {"input": chunk}
        response = requests.post(endpoint, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            embedding = response.json().get("data")[0].get("embedding")
            embeddings.append(embedding)
        else:
            print(f"Embedding generation failed for chunk: {chunk}")
            print(f"Error: {response.text}")  # Debugging line
            raise Exception(f"Embedding generation failed: {response.text}")

    if not embeddings:
        print("No embeddings generated. Please check the Azure endpoint or input text.")

    return embeddings

# Function to create a vector store using Azure OpenAI embeddings
def get_vectorstore(text_chunks, api_key):
    if not text_chunks:
        raise ValueError("No text chunks provided. Make sure that the PDF is processed correctly.")
    
    # Get embeddings from Azure OpenAI
    embeddings_list = get_embeddings_from_azure(text_chunks, api_key)
    if not embeddings_list:
        raise ValueError("No embeddings were generated. Please check the Azure API and input text.")

    # Create the FAISS VectorStore
    embeddings = AzureOpenAIEmbeddings(
        deployment="text-embedding-ada-002",
        api_key=api_key,
        api_version="2023-05-15",
        azure_endpoint="https://api-code-gen.openai.azure.com/"
    )

    # Generate the vector store
    vectorstore = FAISS.from_texts(
        texts=text_chunks,
        embedding=embeddings
    )
    return vectorstore

# Function to create a conversation chain using the vector store
def get_conversation_chain(vectorstore):
    endpoint = os.getenv("ENDPOINT_URL", "https://api-code-gen.openai.azure.com/")  
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo-Code-Generator")  
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "d3c367c33e3f44338f91b767283cc15b")  

    llm = AzureChatOpenAI(
        azure_endpoint=endpoint,
        azure_deployment=deployment,
        openai_api_version="2024-05-01-preview",
        api_key=subscription_key,
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Handle user input and display the chat history
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

# Main function to run the Streamlit app
def DocsWhisper():
    load_dotenv()
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.chat_input("Ask me anything...")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        image_path = './Visualization/assets/Images/logo.png'
    
        # Check if the file exists before trying to display it
        if os.path.exists(image_path):
            st.image(image_path, width=200)
        else:
            st.error("Logo image not found.")
        
        st.sidebar.markdown("<div style='border-bottom:3px solid #fff';width:></div>", unsafe_allow_html=True)

        st.info("Please Upload one or multiple PDFs to start the conversation.")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True,label_visibility="collapsed")
        if st.button("Process"):
            with st.spinner("Processing..."):
                # Get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)
                if not text_chunks:
                    st.error("No text chunks were generated. Please check the PDF content.")
                    return

                # Create vector store
                try:
                    vectorstore = get_vectorstore(text_chunks, "d3c367c33e3f44338f91b767283cc15b")
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                except Exception as e:
                    st.error(f"Error during vectorstore creation: {str(e)}")
                finally:
                    st.success("Processing completed. Start the conversation!")
        
            
                       

if __name__ == '__main__':
    DocsWhisper()

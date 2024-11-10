import streamlit as st
from openai import AzureOpenAI
import os
from Visualization.HelperFun import load_lottie_file
from streamlit_lottie   import st_lottie

# Azure Configuration
endpoint = os.getenv("ENDPOINT_URL", "https://api-code-gen.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo-Code-Generator")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://ai-search-hacka.search.windows.net")
search_key = os.getenv("SEARCH_KEY", "4XXThvjyv6T8DRhXdBGrK7rS5UZUsUh6OamY1HC9qmAzSeDkhB1q")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "d3c367c33e3f44338f91b767283cc15b")
search_index = os.getenv("SEARCH_INDEX_NAME", "mayankindex")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

def AISphere():
    st.markdown("""
        <style>
        .css-18e3th9 {
            padding-top: 0 !important;
        }
        .css-1d391kg {
            padding-top: 0 !important;
        }
        .st-emotion-cache-13ln4jf{
            padding-top: 0 !important;
        }
        .st-emotion-cache-1jicfl2{
            padding-top: 1rem !important;
        }
        .st-emotion-cache-kgpedg{
            padding: 0 !important;
        }
        .st-emotion-cache-7tauuy{
            padding-top: 1rem !important;
        }
        # header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
        
    with st.sidebar:
        image_path = './Visualization/assets/Images/logo.png'
        
        # Check if the file exists before trying to display it
        if os.path.exists(image_path):
            st.image(image_path, width=200)
        else:
            st.error("Logo image not found.")
        
        lottie_json = load_lottie_file("./Visualization/FilesJson/Chatbot.json")    
        st_lottie(lottie_json, speed=1, width=250, height=250, key="initial")
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "system", "content": "Welcome! I'm your chatbot, ready to assist you with anything you need. How can I help you today? 😊"}
        ]



    # Function to display references

    
    # Function to get a response from Azure OpenAI
    def get_response(user_query):
        
        chat_prompt = st.session_state["chat_history"] + [{"role": "user", "content": str(user_query)}]

        # Generate the completion
        completion = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_tokens=500,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False,
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": f"{search_endpoint}",
                            "index_name": search_index,
                            "semantic_configuration": "default",
                            "query_type": "vector_semantic_hybrid",
                            "fields_mapping": {},
                            "in_scope": True,
                            "role_information": "You are an AI assistant that helps people find information.",
                            "filter": None,
                            "strictness": 3,
                            "top_n_documents": 5,
                            "authentication": {
                                "type": "api_key",
                                "key": f"{search_key}"
                            },
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": "text-embedding-ada-002"
                            },
                        }
                    }
                ]
            },
        )
        # Safely access citations
        citations = completion.choices[0].message.context["citations"]
        return [completion.choices[0].message.content, citations[1:3]]



    # Display chat history

    for message in st.session_state["chat_history"]:
        if message["role"] == "system":
            with st.chat_message("System"):
                st.write(message["content"])
        elif message["role"] == "user":
            with st.chat_message("Human"):
                st.write(message["content"])
                
        elif message["role"] == "assistant":
            with st.chat_message("AI"):    
                st.write(message["content"])

    # Display chat history and handle the response as needed

    user_query = st.chat_input("Type your message here...")
    if user_query:
        # Append user's query to chat history (ensure it's a string)
        st.session_state["chat_history"].append({"role": "user", "content": str(user_query)})
        with st.chat_message("Human"):
            st.markdown(user_query)

        # Get AI response and display it
        with st.chat_message("AI"):
            response = get_response(user_query)
            st.write(response[0])  # AI's response
            print(response[0])
            
            

        # Append AI's response to chat history
        st.session_state["chat_history"].append({"role": "assistant", "content": response[0]})

import json 
      
def load_lottie_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lottie_json = json.load(f)
    except UnicodeDecodeError:
        # Handle the error or fallback to a different encoding
        with open(file_path, "r", encoding="latin-1") as f:
            lottie_json = json.load(f)
    return lottie_json


if __name__ == "__main__":
    AISphere()
    
    
    
    
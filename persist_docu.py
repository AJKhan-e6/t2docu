# Import the openai library and os module to set the API key
import openai
import os
from llama_index.llms import OpenAI
from llama_index import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext, load_index_from_storage
)
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores import SimpleVectorStore
import streamlit as st


document_path = '/home/abdul/Downloads/text-to-sql/Talk with documentation/docs/e6-documentation-main'
persistent_path = '/home/abdul/Downloads/text-to-sql/Talk with documentation/stores'

# Initialising streamlit page
st.set_page_config(page_title="Chat with the e6data docs", layout="centered", initial_sidebar_state="auto", menu_items=None)

# Add your openai api key here 
# openai.api_key=
st.title("Chat with the e6data docs💬")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the e6 engine!"}
    ]

@st.cache_resource(show_spinner=False)

def load_data(persistent=True):
     
    
    index = None
    
    service_context = ServiceContext.from_defaults(llm=OpenAI(temperature=0, model="gpt-4-1106-preview", system_prompt="You are an expert on the e6data documentation and your job is to answer technical questions. Assume that all questions are related to the e6data engine. Keep your answers technical and based on facts – do not hallucinate features."))

    if persistent:
        print("started the loading document process...")
        print("Fetching indexed document...")
        storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore.from_persist_dir(persist_dir=persistent_path),
            vector_store=SimpleVectorStore.from_persist_dir(
                persist_dir=persistent_path
            ),
            index_store=SimpleIndexStore.from_persist_dir(persist_dir=persistent_path),
        )
        print("Fetched index process...")
        index = load_index_from_storage(storage_context)
        print("Loading Context ...")
    else:
        print("started the loading document process...")
        documents = SimpleDirectoryReader(document_path, exclude_hidden=True, recursive=True).load_data()
        print("started the indexing process...")
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        print("Persisting the index ...")
        index.storage_context.persist(persist_dir=persistent_path)
	
    return index

index = load_data()


if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
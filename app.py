import streamlit as st
from dotenv import load_dotenv
import os
from openai import AuthenticationError

import chromadb
from chromadb.config import Settings
from text_extractor import get_text_from_files
from vector_store import get_text_chunks, get_vector_store
from openai_qa import check_openai_api_key, get_openai_response

# Load environment variables
load_dotenv()

def main():
    # Check for OpenAI API key
    try:
        check_openai_api_key()
    except ValueError as e:
        st.error(e)
        return

    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.header("Chat with your Documents 💬")

    # Initialize session state
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chroma_client" not in st.session_state:
        st.session_state.chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if user_question := st.chat_input("Ask a question about your documents:"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)

        if st.session_state.vector_store:
            with st.spinner("Searching for answers..."):
                try:
                    # Perform similarity search
                    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 5})
                    docs = retriever.invoke(user_question)

                    # Get response from OpenAI
                    response = get_openai_response(user_question, docs)

                    # Display assistant response and add to history
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except AuthenticationError:
                    error_message = "Authentication Error: Please check your OpenAI API key. It might be invalid or expired."
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
                except Exception as e:
                    error_message = f"An unexpected error occurred: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
        else:
            warning_message = "Please upload and process your documents first."
            st.warning(warning_message)
            st.session_state.messages.append({"role": "assistant", "content": warning_message})

    # Sidebar for file upload
    with st.sidebar:
        st.subheader("Your documents")
        uploaded_files = st.file_uploader(
            "Upload your files here and click on 'Process'", accept_multiple_files=True, type=["pdf", "docx", "pptx", "txt"])
        
        if st.button("Process"):
            if uploaded_files:
                with st.spinner("Processing..."):
                    raw_text = get_text_from_files(uploaded_files)
                    text_chunks = get_text_chunks(raw_text)
                    st.session_state.vector_store = get_vector_store(text_chunks, st.session_state.chroma_client)
                    st.success("Done! You can now ask questions about your documents.")
                    # Clear previous chat history
                    st.session_state.messages = []
            else:
                st.warning("Please upload at least one file.")

if __name__ == '__main__':
    main()
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
import chromadb
import os

COLLECTION_NAME = "rag_chatbot_collection"

def get_text_chunks(text: str) -> list:
    """
    Splits a long text into smaller chunks.

    Args:
        text (str): The input text.

    Returns:
        list: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks: list, client: chromadb.Client):
    """
    Creates a vector store from text chunks using OpenAI's embeddings.

    Args:
        text_chunks (list): A list of text chunks.
        client (chromadb.Client): The ChromaDB client instance.
    """
    # Use the OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # If the collection already exists, delete it to ensure a fresh start.
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(name=COLLECTION_NAME)

    vector_store = Chroma.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        client=client,
        collection_name=COLLECTION_NAME
    )
    return vector_store
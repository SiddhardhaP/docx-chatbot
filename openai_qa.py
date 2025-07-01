import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def check_openai_api_key():
    """Checks for the OpenAI API key in environment variables."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

def get_openai_response(question: str, context_chunks: list):
    """
    Generates a response from the OpenAI model based on the question and context.

    Args:
        question (str): The user's question.
        context_chunks (list): A list of relevant LangChain Document objects.

    Returns:
        str: The model's generated answer.
    """
    # The retriever returns Document objects. We need to extract the page_content.
    context = "\n".join(chunk.page_content for chunk in context_chunks)

    template = """
    Answer the following question based only on the provided context. If the answer is not in the context, say "I don't have enough information to answer that question."
    
    Context:
    {context}
    
    Question:
    {question}
    """

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    
    # Use the modern LCEL (LangChain Expression Language) chain syntax
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    
    response = chain.invoke({"context": context, "question": question})
    
    return response
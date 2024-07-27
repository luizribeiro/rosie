from langchain_community.chat_models.ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


LLMS = {
    "gpt-4o": lambda: ChatOpenAI(model="gpt-4o-2024-05-13"),
    "llama3.1-8b": lambda: ChatOllama(model="llama3.1:8b"),
    "llama3.1-70b": lambda: ChatOllama(model="llama3.1:70b"),
    # TODO: not sure why I'm getting a pyright error without passing stop_sequences
    "groq-70b": lambda: ChatGroq(model="llama-3.1-70b-versatile", stop_sequences=None),
}

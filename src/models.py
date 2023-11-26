from langchain.chat_models import ChatOllama, ChatOpenAI


LLMS = {
    "gpt-3.5": lambda: ChatOpenAI(model_name="gpt-3.5-turbo-1106"),
    "gpt-4": lambda: ChatOpenAI(model_name="gpt-4-1106-preview"),
    "mistral": lambda: ChatOllama(model="mistral:7b-instruct-q5_1"),
    "llama2": lambda: ChatOllama(model="llama2:13b-chat-q4_0"),
}

from langchain.chat_models import ChatOllama, ChatOpenAI


LLMS = {
    "gpt-3.5": lambda: ChatOpenAI(model="gpt-3.5-turbo-1106"),
    "gpt-4": lambda: ChatOpenAI(model="gpt-4-1106-preview"),
    "mistral": lambda: ChatOllama(model="mistral:7b-instruct-q6_K"),
    "llama2": lambda: ChatOllama(model="llama2:13b-chat-q4_0"),
    "starling": lambda: ChatOllama(model="starling-lm:7b-alpha-q8_0"),
}

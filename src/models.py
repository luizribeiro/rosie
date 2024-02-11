from langchain.chat_models import ChatOllama, ChatOpenAI
from typing import Optional, TypeVar


# I don't quite understand why this is needed, but it is
T = TypeVar("T")
def none_throws(x: Optional[T]) -> T:
    if x is None:
        raise ValueError("Expected a non-None value")
    return x
ChatOpenAI = none_throws(ChatOpenAI)
ChatOllama = none_throws(ChatOllama)

LLMS = {
    "gpt-3.5": lambda: ChatOpenAI(model="gpt-3.5-turbo-1106"),
    "gpt-4": lambda: ChatOpenAI(model="gpt-4-1106-preview"),
    "mistral": lambda: ChatOllama(model="mistral:7b-instruct-q6_K"),
    "llama2": lambda: ChatOllama(model="llama2:13b-chat-q4_0"),
    "starling": lambda: ChatOllama(model="starling-lm:7b-alpha-q8_0"),
}

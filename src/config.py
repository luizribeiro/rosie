from langchain.chat_models import ChatOpenAI


LLMS = {
    "gpt-3.5": lambda: ChatOpenAI(model_name="gpt-3.5-turbo-1106"),
    "gpt-4": lambda: ChatOpenAI(model_name="gpt-4-1106-preview"),
}

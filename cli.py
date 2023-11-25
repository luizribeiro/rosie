import asyncio
import typer

from langchain.chat_models import ChatOpenAI

from agent import Rosie
from utils import run_async


LLMS = {
    "gpt-3.5": lambda: ChatOpenAI(model_name="gpt-3.5-turbo-1106"),
    "gpt-4": lambda: ChatOpenAI(model_name="gpt-4-1106-preview"),
}


@run_async
async def main(model: str = "gpt-3.5"):
    llm = LLMS[model]()
    agent = Rosie.create(llm)
    while prompt := input(">> "):
        if prompt == "exit":
            break
        response = await agent.ask(prompt)
        print(response["output"])

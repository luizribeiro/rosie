import asyncio
import typer

from agent import Rosie
from config import LLMS
from utils import run_async


@run_async
async def main(model: str = "gpt-3.5", verbose: bool = False):
    llm = LLMS[model]()
    agent = Rosie.create(llm, verbose=verbose)
    while prompt := input(">> "):
        if prompt == "exit":
            break
        response = await agent.ask(prompt)
        print(response["output"])

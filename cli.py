import asyncio
import typer

from agent import Rosie
from config import LLMS
from utils import run_async


app = typer.Typer()


@app.command()
@run_async
async def chat(model: str = "gpt-3.5", verbose: bool = False):
    llm = LLMS[model]()
    agent = Rosie.create(llm, verbose=verbose)
    while prompt := input("You: "):
        if prompt == "exit":
            break
        response = await agent.ask(prompt)
        print(f"Rosie: {response['output']}")


@app.command()
@run_async
async def serve():
    raise NotImplementedError

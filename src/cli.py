import asyncio

import typer
import uvicorn

from agent import Rosie
from models import LLMS
from utils import run_async
from web import app as web_app


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
async def serve(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = False,
    log_level: str = "debug",
) -> None:
    config = uvicorn.Config(
        web_app,
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
    )
    server = uvicorn.Server(config)
    await server.serve()

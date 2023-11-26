from fastapi import FastAPI

from agent import Rosie
from models import LLMS


app = FastAPI()
# TODO: take this from a config
llm = LLMS["gpt-3.5"]()
agent = Rosie.create(llm)


@app.get("/query")
async def query(prompt: str):
    response = await agent.ask(prompt)
    return {"response": response["output"]}

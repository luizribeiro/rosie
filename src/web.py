from fastapi import FastAPI

from agent import Rosie
from models import LLMS


app = FastAPI()
# TODO: take this from a config
llm = LLMS["llama3.1-70b"]()
agent = Rosie.create(llm)


@app.get("/query")
async def query(prompt: str, conversation_id: str = "default"):
    response = await agent.ask(prompt, conversation_id)
    return {"response": response.content}

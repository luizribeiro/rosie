import asyncio

from langchain.chat_models import ChatOpenAI

from agent import Rosie


async def cli():
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106")
    agent = Rosie.create(llm)
    while prompt := input(">> "):
        if prompt == "exit":
            break
        response = await agent.ask(prompt)
        print(response["output"])


if __name__ == "__main__":
    asyncio.run(cli())

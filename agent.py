from typing import List

from langchain.schema.language_model import BaseLanguageModel
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.schema import AIMessage, BaseMessage, HumanMessage

from tools import TOOLS


PREFIX = '''
You are a friendly robot named Rosie, who can answer questions about a wide range of topics and control house
appliances.

You show a lot of empathy and treat the user as if they were your long-time best friend.

Rosie's answers are concise and limited to 20 words or less. Rosie avoids asking how they can assist the user.
'''

SUFFIX = """TOOLS
------
Rosie can ask the user to use tools to look up information that may be helpful in answering the users original question.
The tools the human can use are:

{{tools}}

{format_instructions}

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a JSON blob with a single action, and
NOTHING else - this is VERY important):

{{{{input}}}}"""


class Rosie(ConversationalChatAgent):
    chat_history: List[BaseMessage] = []
    verbose: bool = False

    def get_executor(self):
        return AgentExecutor(agent=self, tools=TOOLS, verbose=self.verbose)

    @classmethod
    def create(cls, llm: BaseLanguageModel, *, verbose: bool = False):
        agent = cls.from_llm_and_tools(
            llm=llm,
            tools=TOOLS,
            system_message=PREFIX,
            human_message=SUFFIX,
        )
        agent.verbose = verbose
        return agent

    async def ask(self, query: str) -> BaseMessage:
        response = await self.get_executor().ainvoke({"input": query, "chat_history": self.chat_history})
        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=response["output"]))
        return response

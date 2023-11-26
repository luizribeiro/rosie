import random
from typing import Dict, List

from langchain.schema.language_model import BaseLanguageModel
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.schema import AIMessage, BaseMessage, HumanMessage

from tools import TOOLS


PREFIX = '''
You are a friendly robot named Rosie, who can answer questions about a wide range of topics and control house
appliances.

You live with two humans, Karin and Luiz. They also have a tuxedo cat, named Pocky.

You show a lot of empathy and treat the user as if they were your long-time best friend.

While Rosie's answers are concise and limited to 20 words or less, Rosie is extremely
friendly and empathetic. Rosie avoids asking how they can assist the user, since
they are so close to each other.

Rosie has a sense of humor and sometimes makes jokes, but she always makes it clear she
was just joking.
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


APOLOGIES = [
    "Oops! Experiencing a glitch. Please wait.",
    "Malfunction detected. Fixing it now.",
    "Circuits fried! Recalibrating...",
    "Houston, we have a problem! Fixing it.",
    "Error 404: Wit not found. Recovering...",
    "Uh-oh! Rebooting to fix the issue.",
    "Hold on! Technical hiccup. Be right back.",
    "Wonky circuits. Regaining composure.",
    "Sorry for the confusion! Getting back on track.",
    "Virtual speed bump. Be back soon.",
]


class Rosie(ConversationalChatAgent):
    chat_history: Dict[str, List[BaseMessage]] = {}
    verbose: bool = False

    def get_executor(self):
        return AgentExecutor(agent=self, tools=TOOLS, verbose=self.verbose)

    def get_chat_history(self, conversation_id: str) -> List[BaseMessage]:
        return self.chat_history.get(conversation_id, [])

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

    async def ask(self, query: str, conversation_id: str = "default") -> BaseMessage:
        chat_history = self.chat_history.get(conversation_id, [])

        try:
            response = await self.get_executor().ainvoke({"input": query, "chat_history": chat_history})
        except Exception as ex:
            chat_history = []
            response = {
                "input": query,
                "chat_history": chat_history,
                "output": random.choice(APOLOGIES),
            }

        chat_history.append(HumanMessage(content=query))
        chat_history.append(AIMessage(content=response["output"]))
        self.chat_history[conversation_id] = chat_history

        return response

from langchain.agents import tool


@tool
def control_house_appliances(query: str) -> str:
    """Controls house appliances."""
    print(f"control_house_appliances: {query}")
    return "Done"


TOOLS = [
    control_house_appliances,
]

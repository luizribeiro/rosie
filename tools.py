from langchain.agents import tool


@tool
async def control_house_appliances(query: str) -> str:
    """Controls house appliances."""
    print(f"control_house_appliances: {query}")
    return "Error: Unknown appliance."


TOOLS = [
    control_house_appliances,
]

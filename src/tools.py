from langchain.agents import tool


@tool
async def control_house_appliances(query: str) -> str:
    """Controls house appliances."""
    print(f"control_house_appliances: {query}")
    return "Error: Unknown appliance."


@tool
async def current_time(timezone: str) -> str:
    """
    Use this to fetch the current time. Pass into it the timezone you want time for.
    Use the timezone name, not the offset - such as America/New_York.
    If unsure of the location, just default to America/New_York.
    """
    from datetime import datetime
    import pytz
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")


TOOLS = [
    control_house_appliances,
    current_time,
]

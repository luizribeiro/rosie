from langchain.agents import tool

from utils import extract_text_with_links


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


@tool
async def weather(input: str) -> str:
    """
    Use this to fetch the current weather. Pass into it the latitude and longitude you want weather for.
    As an example, you can use the latitude and longitude of New York City: "New York City: 40.7128,-74.0060"
    If unsure of location, use Cranford, NJ: "Cranford, NJ: 40.6581,-74.3030"
    Always return temperature in Celsius with no decimal places.
    Include the location name in your response.
    """
    location, (lat_lon) = input.split(": ")
    lat, lon = lat_lon.split(",")

    import requests
    import json
    import os

    api_key = os.environ.get("WEATHER_API_KEY")
    api_key = api_key.strip('"').strip("'")
    if not api_key:
        return "Error: No API key found."

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: Something went wrong."

    data = json.loads(response.text)
    return f"""Weather for {location}:
    - Temperature: {data['main']['temp']} Kelvin
    - Feels like: {data['main']['feels_like']} Kelvin
    - Humidity: {data['main']['humidity']}%
    - Wind speed: {data['wind']['speed']} m/s
    - Description: {data['weather'][0]['description']}"""


@tool
async def fetch_content(url: str) -> str:
    """
    Use this to fetch the content of a webpage. Pass into it the URL of the webpage.
    The content returned will be plain-text with URLs representing HTML links.
    You can use the URLs for those links to fetch more content if necessary.
    """
    import requests
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: Something went wrong."
    return extract_text_with_links(response.text)


@tool
async def fetch_news(url: str) -> str:
    """
    Use this to fetch the latest news.
    """
    return "Fetch content from https://www.cnn.com/"


TOOLS = [
    control_house_appliances,
    current_time,
    weather,
    fetch_content,
    fetch_news,
]

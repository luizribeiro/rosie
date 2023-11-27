import json
import os
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qs

import aiohttp
import pytz
from langchain.agents import tool

from utils import cached, extract_text_with_links, send_mqtt_message


@tool
async def home_assistant(raw_url: str) -> str:
    """
    Use this to control home automation through Home Assistant.

    The URL passed in should be a valid Home Assistant API call.
    Use https://home.thepromisedlan.club/ as the host for Home Assistant.
    You can assume the API token will be populated.

    Here's an overview of the areas, devices and their entities in this smart home:

    # Office
    - Office 1 Left Window (Roller shade (WM25L-Z))
       - cover.office_1_left_window
    - Office 1 Right Window (Roller shade (WM25L-Z))
       - cover.office_1_right_window
    - Office 1 Ceiling (Inovelli 2-in-1 switch + dimmer (VZM31-SN))
       - light.office_1_ceiling
    - 55" TCL Roku TV (55S555)
       - media_player.55_tcl_roku_tv
       - remote.55_tcl_roku_tv
    """
    # TODO: fetch entities above from the API
    # TODO: allow for GET requests too for fetching state
    # TODO: allow for LLM to provide the data (so multiple entity_ids are supported)
    hass_token = os.environ.get("HASS_TOKEN")

    parsed_url = urlparse(raw_url)
    url = urlunparse(parsed_url._replace(query=''))
    data = parse_qs(parsed_url.query)

    headers = {
        "Authorization": f"Bearer {hass_token}",
        "Content-Type": "application/json",
    }
    json_data = json.dumps(data)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json_data, headers=headers) as response:
                if response.status != 200:
                    text = await response.text()
                    return "Error: Something went wrong."
                data = await response.json()
                return json.dumps(data, indent=2)
    except Exception as e:
        return "Error: Something went wrong."


@tool
async def current_time(timezone: str) -> str:
    """
    Use this to fetch the current time. Pass into it the timezone you want time for.
    Use the timezone name, not the offset - such as America/New_York.
    If unsure of the location, just default to America/New_York.
    """
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")


@tool
@cached
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
    print("calling weather api")

    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        return "Error: No OpenWeatherMap API key setup."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                return "Error: Something went wrong."
            data = await response.json()
            return f"""Weather for {location}:
            - Temperature: {data['main']['temp']} Kelvin
            - Feels like: {data['main']['feels_like']} Kelvin
            - Humidity: {data['main']['humidity']}%
            - Wind speed: {data['wind']['speed']} m/s
            - Description: {data['weather'][0]['description']}"""


@tool
@cached
async def fetch_content(url: str) -> str:
    """
    Use this to fetch the content of a webpage. Pass into it the URL of the webpage.
    The content returned will be plain-text with URLs representing HTML links.
    You can use the URLs for those links to fetch more content if necessary.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return "Error: Something went wrong."
            return extract_text_with_links(await response.text())
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


@tool
async def send_to_user(message: str) -> str:
    """
    Use this to send a notification to the user's phone.
    """
    payload = {
        "topic": "rosie",
        "title": "From Rosie",
        "message": message,
    }
    return await send_mqtt_message("ntfy/publish", payload)


TOOLS = [
    home_assistant,
    current_time,
    weather,
    fetch_content,
    fetch_news,
    send_to_user,
]

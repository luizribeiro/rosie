import asyncio
import json
import os
import re
from functools import wraps
from typing import Dict

import aiomqtt
from bs4 import BeautifulSoup, Comment


def run_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        async def coro_wrapper():
            return await func(*args, **kwargs)

        return asyncio.run(coro_wrapper())

    return wrapper


def extract_text_with_links(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    # append the text to the link
    for a in soup.select('a[href]'):
        a.contents.append(soup.new_string(' ({})'.format(a['href'])))

    for script in soup.find_all('script'):
        script.decompose()

    for style in soup.find_all('style'):
        style.decompose()

    for link in soup.find_all('link'):
        link.decompose()

    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # unwrap() all tags
    for tag in soup.select('*'):
        tag.unwrap()

    content = str(soup)
    trimmed_content = re.sub(' +', ' ', content)
    trimmed_content = re.sub("\n+", "\n", trimmed_content)
    return trimmed_content.strip()


async def send_mqtt_message(topic: str, payload: Dict[str, str]) -> str:
    broker_address = os.environ.get("MQTT_HOST")
    try:
        async with aiomqtt.Client(broker_address) as client:
            await client.publish(topic, payload=json.dumps(payload))
        return "Success!"
    except Exception as e:
        return f"Error: {e}"

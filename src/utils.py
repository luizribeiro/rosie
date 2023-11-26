import asyncio
import json
import os
import re
from functools import wraps
from typing import Dict

from bs4 import BeautifulSoup, Comment
import paho.mqtt.client as mqtt


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


# TODO: make this async
def send_mqtt_message(topic: str, payload: Dict[str, str]) -> str:
    # TODO: make this configurable
    broker_address = "127.0.0.1"
    if not broker_address:
        return "Error: No MQTT broker address found."
    client = mqtt.Client("rosie")
    try:
        client.connect(broker_address)
        client.publish(topic, payload=json.dumps(payload))
    except Exception as e:
        return f"Error: {e}"
    client.disconnect()
    return "Success!"

import json
import requests
from urllib.parse import urlencode
from rich.console import Console
from geopy.distance import geodesic
from deep_translator import GoogleTranslator


console = Console()
translator = GoogleTranslator(source="auto", target="en")

def get_website_config(name: str):
    with open("./config.json", "r") as file:
        config = json.load(file)
    return config[name]

def calculate_driving_distance(origin: tuple, destination: tuple):
    distance = geodesic(origin, destination).kilometers
    return f"{distance:.2f} km"

def send_telegram_message(bot_token: str, admin_id: int, message: str):
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": admin_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(base_url, data=payload)
    return response.json()

def translate_to_english(text):
    """Translate text to English using Google Translator."""
    return translator.translate(text)

def create_urls(config: dict, url_number: int = 5, limit: int = 100):
    urls = []
    for i in range(url_number):
        query_params = config.copy()
        query_params["offset"] = i * limit
        query_params["limit"] = limit

        url = f"{config.get('api_link', '')}?{urlencode(query_params)}"
        urls.append(url)

    return urls
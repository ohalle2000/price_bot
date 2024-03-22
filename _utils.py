import json
import requests
from urllib.parse import urlencode
from rich.console import Console
from geopy.distance import geodesic
from deep_translator import GoogleTranslator
from _secrets import BOT_TOKEN, CHAT_ID1, CHAT_ID2, CHAT_ID3


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
    try:
        translated_text = translator.translate(text.encode("utf-8", "replace").decode("utf-8"))
    except Exception as e:
        console.log(f"Error in translation: {e}")
        translated_text = text
    return translated_text


def create_urls(config: dict, url_number: int = 5, limit: int = 100):
    urls = []
    for i in range(url_number):
        query_params = config.copy()
        query_params.pop("main_link", None)
        query_params["offset"] = i * limit
        query_params["limit"] = limit

        api_link = query_params.pop("api_link")

        url = f"{api_link}?{urlencode(query_params)}"
        urls.append(url)

    return urls


def send_errors_to_all_chats(e: Exception):
    for chat_id in [CHAT_ID1, CHAT_ID2, CHAT_ID3]:
        send_telegram_message(BOT_TOKEN, chat_id, f"bot error: {e}")

import json
import requests
from urllib.parse import urlencode
from rich.console import Console
from geopy.distance import geodesic
from deep_translator import GoogleTranslator
from _secrets import BOT_TOKEN, CHAT_ID1, CHAT_ID2, CHAT_ID3


console = Console()
translator = GoogleTranslator(source="auto", target="en")

template_config = {
    "source": str,
    "max_price": int,
    "chat_id": str,
    "allowed_models": (type(None), list),
    "url_numbers": int,
    "function_for_message": callable,
    "api_link": str,
    "query_params": dict,
}


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


def create_urls(config: dict, limit: int = 100):
    urls = []
    for i in range(config["url_numbers"]):
        query_params = config["query_params"].copy()
        query_params["offset"] = i * limit
        query_params["limit"] = limit

        url = f"{config["api_link"]}?{urlencode(query_params)}"
        urls.append(url)

    return urls


def send_errors_to_all_chats(e: Exception):
    for chat_id in [CHAT_ID1, CHAT_ID2, CHAT_ID3]:
        send_telegram_message(BOT_TOKEN, chat_id, f"bot error: {e}")


def get_int_from_itemId(item_id: str):
    return int(item_id[1:])

def validate_config(config):
    for t_key, t_value in template_config.items():
        if t_key not in config:
            raise ValueError(f"Key '{t_key}' missing in configuration")

        if t_key == 'function_for_message':
            if not callable(config[t_key]):
                raise TypeError(f"The '{t_key}' should be a callable (function). Got: {type(config[t_key]).__name__}")
        else:
            if not isinstance(config[t_key], t_value):
                raise TypeError(f"Incorrect type for key '{t_key}'. Expected {t_value.__name__}, got {type(config[t_key]).__name__}")
            
    console.print(f"Configuration for {config['source']} is valid")

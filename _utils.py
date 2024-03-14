import json
import requests
from rich.console import Console

console = Console()


def get_website_config(name: str):
    with open("./config.json", "r") as file:
        config = json.load(file)
    return config[name]


def send_telegram_message(bot_token: str, admin_id: int, message: str):
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": admin_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(base_url, data=payload)
    return response.json()

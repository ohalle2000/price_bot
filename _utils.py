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


def open_file(file_path: str):
    """Read lines from a file or create it if not exists."""
    try:
        with open(file_path, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


def write_file(file_path: str, data1: list, data2: list):
    """Write list of data to a file, each on a new line."""
    with open(file_path, "w") as file:
        file.write("\n".join(data1 + data2))

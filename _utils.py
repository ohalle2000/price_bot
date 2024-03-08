import json
import requests
from rich.console import Console

console = Console()


def get_website_config(name: str):
    with open("./config.json", "r") as file:
        config = json.load(file)
    return config["websites"][name]


def send_telegram_message(bot_token: str, admin_id: int, message: str):
    base_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": admin_id, "text": message}
    response = requests.post(base_url, data=payload)
    return response.json()


def expand_link_with_pages(link: str, test_to_expand: str, number_of_pages: int) -> list:
    links = []
    links.append(link + test_to_expand)
    for i in range(1, number_of_pages + 1):
        result_link = link + f"p/{i}/" + test_to_expand
        links.append(result_link)
    return links


def custom_sort(link):
    return ("https" in link, link)

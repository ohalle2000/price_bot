import requests
import time
import markdown2
from urllib.parse import urlencode, quote
from _utils import open_file, write_file, get_website_config, send_telegram_message
from _secrets import BOT_TOKEN, ADMIN_ID
from deep_translator import GoogleTranslator
from rich.console import Console

# Constants
SLEEP_TIME = 60
LIMIT = 100
CAR_FILE = "./cars2.txt"
CONFIG_SOURCE = "cars-2dehands"

console = Console()
translator = GoogleTranslator(source="auto", target="en")


def translate_to_english(text):
    """Translate text to English using Google Translator."""
    return translator.translate(text)


def escape_markdown(text):
    """Escape special characters for MarkdownV2"""
    escape_chars = "_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)


def create_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    listing_url = f"{config['main_link']}{car['vipUrl']}"

    car_attributes = {attr["key"]: attr["value"] for attr in car["attributes"]}

    model = car["vipUrl"].split("/")[3]

    message = f"🚗 **New Car Listing Found!**\n"
    message += f"#{model}\n"
    message += f"🚘 Title: {translate_to_english(car['title'])}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"📍 Location: {car['location']['cityName']}, {car['location']['countryName']}\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f"📅 Year: {car_attributes.get('constructionYear')}\n"
    message += f"🛣️ Km: {car_attributes.get('mileage', 'N/A')} km\n"
    message += f"⛽ Fuel: {car_attributes.get('fuel', 'N/A')}\n"
    message += f'🔗 <a href="{listing_url}">View Listing</a>\n'
    return message


def create_urls(url_number: int = 5, config: dict = None, limit: int = 100):
    if config is None:
        config = {}

    urls = []
    for i in range(url_number):
        query_params = config.copy()
        query_params["offset"] = i * limit
        query_params["limit"] = limit

        url = f"{config.get('api_link', '')}?{urlencode(query_params)}"
        urls.append(url)

    return urls


def main():
    config = get_website_config(CONFIG_SOURCE)
    urls = create_urls(url_number=5, config=config, limit=LIMIT)

    while True:
        try:
            cars = (item for url in urls for item in requests.get(url).json()["listings"])
            filtered_cars = [car for car in cars if car["priceInfo"]["priceCents"] <= config["max_price"]]

            sorted_cars = sorted(filtered_cars, key=lambda x: x["itemId"], reverse=True)[:100]
            checked_cars = open_file(CAR_FILE)

            new_cars = [car for car in sorted_cars if car["itemId"] not in checked_cars]
            for car in new_cars:
                bot_message = create_bot_message(car, config)
                print(bot_message)
                send_telegram_message(BOT_TOKEN, ADMIN_ID, bot_message)

            write_file(CAR_FILE, [car["itemId"] for car in new_cars], checked_cars)

        except requests.RequestException as e:
            console.log(f"Error fetching data: {e}")

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()

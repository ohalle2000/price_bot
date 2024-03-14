import time
import requests
from rich.console import Console
from urllib.parse import urlencode
from geopy.distance import geodesic
from deep_translator import GoogleTranslator

from _utils import get_website_config, send_telegram_message
from _secrets import BOT_TOKEN, ADMIN_ID

# Constants
SLEEP_TIME = 60
LIMIT = 100
CONFIG_SOURCE = "cars-2dehands"

NIJMEGEN = (51.8433, 5.8609)
LEUVEN = (50.8823, 4.7138)
console = Console()

translator = GoogleTranslator(source="auto", target="en")


def translate_to_english(text):
    """Translate text to English using Google Translator."""
    return translator.translate(text)


def calculate_driving_distance(origin: tuple, destination: tuple):
    distance = geodesic(origin, destination).kilometers
    return f"{distance:.2f} km"


def escape_markdown(text):
    """Escape special characters for MarkdownV2"""
    escape_chars = "_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)


def create_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    listing_url = f"{config['main_link']}{car['vipUrl']}"
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]

    distance_nijmegen = calculate_driving_distance(NIJMEGEN, (lat, long))
    distance_leuven = calculate_driving_distance(LEUVEN, (lat, long))

    car_attributes = {attr["key"]: attr["value"] for attr in car["attributes"]}

    model = car["vipUrl"].split("/")[3]

    message = f"🚗 **New Car Listing Found!**\n"
    message += f"#{model}\n"
    message += f"🚘 Title: {translate_to_english(car['title'])}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"📍 Location: {car['location']['cityName']}, {car['location']['countryName']}\n"
    message += f"📍 Distance Nijmegen: {distance_nijmegen}, Leuven: {distance_leuven}\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f"📅 Year: {car_attributes.get('constructionYear')}\n"
    message += f"🛣️ Km: {car_attributes.get('mileage', 'N/A')} km\n"
    message += f"⛽ Fuel: {car_attributes.get('fuel', 'N/A')}\n"
    message += f'🔗 <a href="{listing_url}">View Listing</a>\n'
    return message


def create_urls(config: dict, url_number: int = 5, limit: int = 100):
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
    urls = create_urls(config=config, url_number=30, limit=LIMIT)
    newest_car_id = None

    while True:
        try:
            cars = (item for url in urls for item in requests.get(url).json()["listings"])

            if newest_car_id:
                filtered_cars = [
                    car
                    for car in cars
                    if car["priceInfo"]["priceCents"] <= config["max_price"] and car["itemId"] > newest_car_id
                ]
            else:
                filtered_cars = [car for car in cars if car["priceInfo"]["priceCents"] <= config["max_price"]]

            if not filtered_cars:
                time.sleep(SLEEP_TIME)
                continue

            sorted_cars = sorted(filtered_cars, key=lambda x: int(x["itemId"][1:]), reverse=True)

            if newest_car_id:
                for car in sorted_cars:
                    bot_message = create_bot_message(car, config)
                    send_telegram_message(BOT_TOKEN, ADMIN_ID, bot_message)

            newest_car_id = sorted_cars[0]["itemId"]
            console.print(f"Newest car id: {newest_car_id}")

        except Exception as e:
            console.log(f"Error fetching data: {e}")

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()

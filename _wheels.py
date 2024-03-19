import requests
from _secrets import BOT_TOKEN
from _utils import console, send_telegram_message, translate_to_english, calculate_driving_distance

NIJMEGEN = (51.8433, 5.8609)
LEUVEN = (50.8823, 4.7138)

def create_wheels_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    listing_url = f"{config['main_link']}{car['vipUrl']}"
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]

    distance_nijmegen = calculate_driving_distance(NIJMEGEN, (lat, long))
    distance_leuven = calculate_driving_distance(LEUVEN, (lat, long))

    message = f" **New wheel Listing Found!**\n"
    message += f" Title: {translate_to_english(car['title'])}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"📍 Location: {car['location'].get('cityName')}, {car['location'].get('countryName')}\n"
    message += f"📍 Distance Nijmegen: {distance_nijmegen}, Leuven: {distance_leuven}\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f'🔗 <a href="{listing_url}">View Listing</a>\n'
    return message

def check_cars(config: dict, urls: list, chat_id: str, newest_car_id: str = None):
    new_newest_car_id = newest_car_id
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
            return new_newest_car_id

        sorted_cars = sorted(filtered_cars, key=lambda x: int(x["itemId"][1:]), reverse=True)
        new_newest_car_id = sorted_cars[0]["itemId"]
        console.print(f"Newest car id: {new_newest_car_id}")

        if newest_car_id:
            for car in sorted_cars:
                bot_message = create_wheels_bot_message(car, config)
                send_telegram_message(BOT_TOKEN, chat_id, bot_message)

    except Exception as e:
        console.log(f"Error fetching data: {e}")
        send_telegram_message(BOT_TOKEN, chat_id, f"Error fetching data. Check logs for more info. {e}")
        
    return new_newest_car_id

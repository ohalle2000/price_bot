import requests
from _secrets import BOT_TOKEN
from _utils import console, send_telegram_message, translate_to_english, calculate_driving_distance

NIJMEGEN = (51.8433, 5.8609)
LEUVEN = (50.8823, 4.7138)

def create_car_bot_message(car: dict, config: dict):
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
    message += f"📍 Location: {car['location'].get('cityName')}, {car['location'].get('countryName')}\n"
    message += f"📍 Distance Nijmegen: {distance_nijmegen}, Leuven: {distance_leuven}\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f"📅 Year: {car_attributes.get('constructionYear')}\n"
    message += f"🛣️ Km: {car_attributes.get('mileage', 'N/A')} km\n"
    message += f"⛽ Fuel: {car_attributes.get('fuel', 'N/A')}\n"
    message += f'🔗 <a href="{listing_url}">View Listing</a>\n'
    return message

def check_cars(config: dict, urls: list, chat_id: str, newest_car_id: str = None):
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
            return newest_car_id
    
        sorted_cars = sorted(filtered_cars, key=lambda x: int(x["itemId"][1:]), reverse=True)
    
        if newest_car_id:
            for car in sorted_cars:
                bot_message = create_car_bot_message(car, config)
                send_telegram_message(BOT_TOKEN, chat_id, bot_message)
    
        newest_car_id = sorted_cars[0]["itemId"]
        console.print(f"Newest car id: {newest_car_id}")
    except Exception as e:
        console.log(f"Error fetching data: {e}")
        send_telegram_message(BOT_TOKEN, chat_id, f"Error fetching data. Check logs for more info. {e}")
    return newest_car_id

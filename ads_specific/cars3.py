from tools.utils import translate_to_russian, calculate_driving_distance, NIJMEGEN


def create_cars3_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    main_link = config["api_link"].split("/lrp")[0]
    listing_url = main_link + car["vipUrl"]
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]
    city = car["location"].get("cityName", "N/A")
    country = car["location"].get("countryName", "N/A")

    distance_nijmegen = calculate_driving_distance(NIJMEGEN, (lat, long))

    car_attributes = {attr["key"]: attr["value"] for attr in car["attributes"]}

    model = car["vipUrl"].split("/")[3]

    message = "🚗 **Новая машина найдена!**\n"
    message += f"#{model}\n"
    message += f"🚘 {translate_to_russian(car['title'])}\n"
    message += f"💰 Цена: €{price_euro} ({price_type})\n"
    message += f"📍 Локация: {city}, {country}\n"
    message += f"📍 Расстояние до Nijmegen: {distance_nijmegen:.2f} km\n"
    message += f"🗒️ Описание: {translate_to_russian(car['categorySpecificDescription'])}\n"
    message += f"📅 Год: {car_attributes.get('constructionYear')}\n"
    message += f"🛣️ Km: {car_attributes.get('mileage', 'N/A')} km\n"
    message += f"⛽ Топливо: {car_attributes.get('fuel', 'N/A')}\n"
    message += f'🔗 <a href="{listing_url}">View Listing</a>\n'
    return message

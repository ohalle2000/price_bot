from _utils import translate_to_english, calculate_driving_distance, NIJMEGEN, LEUVEN

def create_basic_bot_message(car: dict, config: dict):
    price_euro = car["priceInfo"]["priceCents"] / 100
    price_type = car["priceInfo"]["priceType"]
    main_link = config["api_link"].split("/lrp")[0]
    listing_url = main_link + car["vipUrl"]
    lat = car["location"]["latitude"]
    long = car["location"]["longitude"]

    distance_nijmegen = calculate_driving_distance(NIJMEGEN, (lat, long))
    distance_leuven = calculate_driving_distance(LEUVEN, (lat, long))

    message = f" **New {config["source"]} Listing Found!**\n"
    message += f" Title: {translate_to_english(car['title'])}\n"
    message += f"💰 Price: €{price_euro} ({price_type})\n"
    message += f"📍 Location: {car['location'].get('cityName', 'N/A')}, {car['location'].get('countryName', 'N/A')}\n"
    message += f"📍 Distance Nijmegen: {distance_nijmegen:.2f} km, Leuven: {distance_leuven:.2f} km\n"
    message += f"🗒️ Description: {translate_to_english(car['categorySpecificDescription'])}\n"
    message += f'🔗 <a href="{listing_url}">View Listing</a>\n'
    return message

import sys
import time
import requests

from _cars import create_cars_bot_message
from _wheels import create_wheels_bot_message
from _utils import get_website_config, create_urls, send_telegram_message, console
from _secrets import BOT_TOKEN, CHAT_ID1, CHAT_ID2, CHAT_ID3

# Constants
SLEEP_TIME = 60
LIMIT = 100
CONFIG_SOURCE1 = "cars-2dehands"
CONFIG_SOURCE2 = "cars-marktplaats"

CONFIG_PRICE1_2 = 500000

CONFIG_SOURCE3 = "wheels-marktplaats"
CONFIG_SOURCE4 = "wheels-2dehands"

CONFIG_PRICE3_4 = 50000

allowed_models = ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"]
CONFIG_PRICE5 = 1000000

def get_ads(urls: list) -> list:
    ads = []
    for url in urls:
        try:
            response = requests.get(url)
            time.sleep(2)
            response.raise_for_status()
            data = response.json()
            ads.extend(data["listings"])
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError for URL {url}: {e}")
            print("Response:", response.text) 
            sys.exit(1)
        except requests.exceptions.JSONDecodeError as e:
            print(f"JSONDecodeError for URL {url}: {e}")
            print("Response:", response.text) 
            sys.exit(1)
        except Exception as e:
            print(f"Error for URL {url}: {e}")
            print("Response:", response.text) 
            sys.exit(1)
    return ads

def filter_ads(ads: list, max_price: int, newest_car_id: str, allowed_models: list = None) -> tuple:
    filtered_ads = []

    for idx, ad in enumerate(ads):
        if ad["priceInfo"]["priceCents"] <= max_price and (newest_car_id is None or ad["itemId"] > newest_car_id):
            model = ad["vipUrl"].split("/")[3] if allowed_models is not None else None

            if allowed_models is None or model in allowed_models:
                console.print(f"Found ad: '{ad['itemId']}' for index of '{idx}' size: '{len(ads)}'")
                filtered_ads.append(ad)

    sorted_ads = sorted(filtered_ads, key=lambda x: int(x["itemId"][1:]), reverse=True)

    if not sorted_ads:
        return newest_car_id, []
    
    console.print(f"Newest id: {sorted_ads[0]["itemId"]}")

    if newest_car_id is None:
        return sorted_ads[0]["itemId"], []

    return sorted_ads[0]["itemId"], sorted_ads


def check_ads(config: dict, filtered_ads: list, chat_id: str, function_for_message):
    try:
        for car in filtered_ads:
            bot_message = function_for_message(car, config)
            send_telegram_message(BOT_TOKEN, chat_id, bot_message)

    except Exception as e:
        console.log(f"Error fetching data: {e}")
        send_telegram_message(BOT_TOKEN, chat_id, f"Error fetching data. Check logs for more info. {e}")


def main():
    config1 = get_website_config(CONFIG_SOURCE1)
    config2 = get_website_config(CONFIG_SOURCE2)
    config3 = get_website_config(CONFIG_SOURCE3)
    config4 = get_website_config(CONFIG_SOURCE4)

    urls1 = create_urls(config=config1, url_number=15, limit=LIMIT)
    urls2 = create_urls(config=config2, url_number=15, limit=LIMIT)
    urls3 = create_urls(config=config3, url_number=2, limit=LIMIT)
    urls4 = create_urls(config=config4, url_number=2, limit=LIMIT)

    newest_car_id_1 = None
    newest_car_id_2 = None
    newest_car_id_3 = None
    newest_car_id_4 = None
    newest_wheel_id_1 = None
    newest_wheel_id_2 = None

    while True:
        ads1 = get_ads(urls1)
        ads3 = ads1.copy()
        newest_car_id_1, ads1 = filter_ads(ads1, CONFIG_PRICE1_2, newest_car_id_1)

        check_ads(
            config=config1,
            filtered_ads=ads1,
            chat_id=CHAT_ID1,
            function_for_message=create_cars_bot_message,
        )

        ads2 = get_ads(urls2)
        ads4 = ads2.copy()
        newest_car_id_2, ads2 = filter_ads(ads2, CONFIG_PRICE1_2, newest_car_id_2)

        check_ads(
            config=config2,
            filtered_ads=ads2,
            chat_id=CHAT_ID1,
            function_for_message=create_cars_bot_message,
        )

        newest_car_id_3, ads3 = filter_ads(ads3, CONFIG_PRICE5, newest_car_id_3, allowed_models)

        check_ads(
            config=config1,
            filtered_ads=ads3,
            chat_id=CHAT_ID2,
            function_for_message=create_cars_bot_message,
        )

        newest_car_id_4, ads4 = filter_ads(ads4, CONFIG_PRICE5, newest_car_id_4, allowed_models)

        check_ads(
            config=config2,
            filtered_ads=ads4,
            chat_id=CHAT_ID2,
            function_for_message=create_cars_bot_message,
        )

        ads5 = get_ads(urls3)
        newest_wheel_id_1, ads5 = filter_ads(ads5, CONFIG_PRICE3_4, newest_wheel_id_1)

        check_ads(
            config=config3,
            filtered_ads=ads5,
            chat_id=CHAT_ID3,
            function_for_message=create_wheels_bot_message,
        )

        ads6 = get_ads(urls4)
        newest_wheel_id_2, ads6 = filter_ads(ads6, CONFIG_PRICE3_4, newest_wheel_id_2)

        check_ads(
            config=config4,
            filtered_ads=ads6,
            chat_id=CHAT_ID3,
            function_for_message=create_wheels_bot_message,
        )

        print(newest_car_id_1, newest_car_id_2, newest_car_id_3, newest_car_id_4, newest_wheel_id_1, newest_wheel_id_2)


if __name__ == "__main__":
    main()

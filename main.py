import sys
import time
import json
import requests
from random import randint

from config import config
from _secrets import BOT_TOKEN
from _utils import create_urls, send_telegram_message, send_errors_to_all_chats, get_int_from_itemId, validate_config, console

LIMIT = 99
SLEEP_TIME = 10
RETRY_TIME = 60

ERROR_CODES = [502, 429]

def get_ads(urls: list) -> list:
    ads = []
    for url in urls:
        try:
            response = requests.get(url)
            time.sleep(randint(0, SLEEP_TIME))
            # check if error code is 502 and sleep for 10 seconds
            if response.status_code in ERROR_CODES:
                console.print(f"Error {response.status_code} for URL {url}")
                time.sleep(RETRY_TIME)
                response = requests.get(url)
            
            response.raise_for_status()
            data = response.json()
            ads.extend(data["listings"])

            # check if there is no more ads in api response
            if len(data["listings"]) < LIMIT:
                break
        except Exception as e:
            print(f"Error for URL {url}: {e}")
            print("Response:", response.text)
            # send_errors_to_all_chats(e)
            sys.exit(1)
    return ads


def filter_ads(ads: list, config: dict) -> tuple:
    filtered_ads = []
    for idx, ad in enumerate(ads):
        ad_id = get_int_from_itemId(ad["itemId"])
        if (config["max_price"] is None or ad["priceInfo"]["priceCents"] <= config["max_price"]) and (
            config["last_id"] is None or ad_id > config["last_id"]
        ):
            model = ad["vipUrl"].split("/")[3] if config["allowed_models"] is not None else None

            if config["allowed_models"] is None or model in config["allowed_models"]:
                if config["last_id"]:
                    console.print(f"Found ad: '{ad_id}' for index of '{idx}' size: '{len(ads)}'")
                filtered_ads.append(ad)

    sorted_ads = sorted(filtered_ads, key=lambda x: int(x["itemId"][1:]), reverse=True)

    if not sorted_ads:
        return []

    last_found_ad_id = get_int_from_itemId(sorted_ads[0]["itemId"])
    console.print(f"Last found add id for {config["source"]}: {last_found_ad_id}")

    # don't send the adds from the first iteration
    if config["last_id"] is None:
        config["last_id"] = last_found_ad_id
        return []

    config["last_id"] = last_found_ad_id
    return sorted_ads


def check_ads(config: dict, filtered_ads: list):
    try:
        for car in filtered_ads:
            bot_message = config["function_for_message"](car, config)
            send_telegram_message(BOT_TOKEN, config["chat_id"], bot_message)
    except Exception as e:
        console.log(f"Error fetching data: {e}")
        send_telegram_message(BOT_TOKEN, config["chat_id"], f"Error fetching data. Check logs for more info. {e}")


def main():

    for add_config in config:
        add_config = config[add_config]
        validate_config(add_config)
        add_config["urls"] = create_urls(config=add_config, limit=LIMIT)
        add_config["last_id"] = None

    while True:
        cache_ads = {}
        for add_config in config:
            add_config = config[add_config]
            cache_key = f"{add_config['api_link']}_{json.dumps(add_config['query_params'], sort_keys=True)}"

            if cache_key in cache_ads:
                ads = cache_ads[cache_key]
            else:
                ads = get_ads(urls=add_config["urls"])
                cache_ads[cache_key] = ads

            ads = filter_ads(ads=ads, config=add_config)
            check_ads(config=add_config, filtered_ads=ads)


if __name__ == "__main__":
    main()

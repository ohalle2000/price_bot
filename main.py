import time

from _cars import check_cars
from _wheels import check_wheels
from _utils import get_website_config, create_urls, console
from _secrets import CHAT_ID1, CHAT_ID2

# Constants
SLEEP_TIME = 60
LIMIT = 100
CONFIG_SOURCE1 = "cars-2dehands"
CONFIG_SOURCE2 = "cars-marktplaats"
CONFIG_SOURCE3 = "wheels-marktplaats"
CONFIG_SOURCE4 = "wheels-2dehands"


def main():
    config1 = get_website_config(CONFIG_SOURCE1)
    config2 = get_website_config(CONFIG_SOURCE2)
    config3 = get_website_config(CONFIG_SOURCE3)
    config4 = get_website_config(CONFIG_SOURCE4)

    urls1 = create_urls(config=config1, url_number=30, limit=LIMIT)
    urls2 = create_urls(config=config2, url_number=30, limit=LIMIT)
    urls3 = create_urls(config=config3, url_number=2, limit=LIMIT)
    urls4 = create_urls(config=config4, url_number=2, limit=LIMIT)

    newest_car_id_1 = None
    newest_car_id_2 = None
    newest_car_id_3 = None
    newest_car_id_4 = None

    while True:
        newest_car_id_1 = check_cars(config=config1, urls=urls1, newest_car_id=newest_car_id_1, chat_id=CHAT_ID1)
        newest_car_id_2 = check_cars(config=config2, urls=urls2, newest_car_id=newest_car_id_2, chat_id=CHAT_ID1)
        newest_car_id_3 = check_wheels(config=config3, urls=urls3, newest_car_id=newest_car_id_3, chat_id=CHAT_ID2)
        newest_car_id_4 = check_wheels(config=config4, urls=urls4, newest_car_id=newest_car_id_4, chat_id=CHAT_ID2)

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()

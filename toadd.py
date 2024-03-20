from _cars import create_cars_bot_message
from _wheels import create_wheels_bot_message
from _secrets import CHAT_ID1, CHAT_ID2, CHAT_ID3

main_config = {
    "cars_2dehands": {
        "source": "cars-2dehands",
        "max_price": 500000,
        "chat_id": CHAT_ID1,
        "allowed_models": None,
        "url_number": 30,
        "function_for_message": create_cars_bot_message,
    },
    "cars_marktplaats": {
        "source": "cars-marktplaats",
        "max_price": 500000,
        "chat_id": CHAT_ID1,
        "allowed_models": None,
        "url_number": 30,
        "function_for_message": create_cars_bot_message,
    },
    "cars_2dehands": {
        "source": "cars-2dehands",
        "max_price": 500000,
        "chat_id": CHAT_ID2,
        "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
        "url_number": 30,
        "function_for_message": create_cars_bot_message,
    },
    "cars_marktplaats": {
        "source": "cars-marktplaats",
        "max_price": 500000,
        "chat_id": CHAT_ID2,
        "allowed_models": ["audi", "volkswagen", "seat", "skoda", "bmw", "mini", "lexus"],
        "url_number": 30,
        "function_for_message": create_cars_bot_message,
    },
    "wheels_2dehands": {
        "source": "wheels-2dehands",
        "max_price": 50000,
        "chat_id": CHAT_ID3,
        "url_number": 2,
        "function_for_message": create_wheels_bot_message,
    },
    "wheels_marktplaats": {
        "source": "wheels-marktplaats",
        "max_price": 50000,
        "chat_id": CHAT_ID3,
        "url_number": 2,
        "function_for_message": create_wheels_bot_message,
    },
}

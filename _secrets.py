import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID1 = os.getenv("CHAT_ID1")
CHAT_ID2 = os.getenv("CHAT_ID2")
CHAT_ID3 = os.getenv("CHAT_ID3")


if not BOT_TOKEN or not CHAT_ID1:
    raise Exception("BOT_TOKEN or ADMIN_ID is not set")

if not CHAT_ID2:
    print("WARNING: CHAT_ID2 is not set.")
    CHAT_ID2 = CHAT_ID1

if not CHAT_ID3:
    print("WARNING: CHAT_ID3 is not set.")
    CHAT_ID3 = CHAT_ID1

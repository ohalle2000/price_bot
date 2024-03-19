import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID1 = os.getenv("CHAT_ID1")
CHAT_ID2 = os.getenv("CHAT_ID2")


if not BOT_TOKEN or not CHAT_ID1:
    raise Exception("BOT_TOKEN or ADMIN_ID is not set")

if not CHAT_ID2:
    print("WARNING: CHAT_ID2 is not set.")

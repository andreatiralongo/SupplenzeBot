import os

URL = os.getenv("URL")
TEXT_SEARCH = os.getenv("TEXT_SEARCH")
API_KEY = os.getenv("TELEGRAM_TOKEN")
MINUTES_TIMEOUT = 15

CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS").split(",")
import time

import requests
from bs4 import BeautifulSoup
import os
from config import URL, TEXT_SEARCH, API_KEY, TELEGRAM_CHAT_IDS

# File to store previously seen links
seen_file = "seen_links.txt"

def check_new_assistenze():
    # Load previously seen links
    if os.path.exists(seen_file):
        with open(seen_file, "r") as f:
            seen_links = set(line.strip() for line in f)
    else:
        seen_links = set()

    # Fetch the page
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        exit()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> tags containing the search text
    current_links = set()
    for a_tag in soup.find_all("a"):
        if TEXT_SEARCH in a_tag.text.strip():  # partial match
            href = a_tag.get("href")
            if href:
                current_links.add(href)

    # Find new links
    new_links = current_links - seen_links

    # Print new links
    if new_links:
        for new_link in new_links:
            message = "Nuova assistenza:\n" + new_link

            # ---------------- SEND TO MULTIPLE TELEGRAM CHATS ----------------
            telegram_url = f"https://api.telegram.org/bot{API_KEY}/sendMessage"
            for chat_id in TELEGRAM_CHAT_IDS:
                payload = {
                    "chat_id": chat_id,
                    "text": message
                }
                r = requests.post(telegram_url, data=payload)
                if r.status_code == 200:
                    print(f"Message sent to {chat_id} successfully!")
                else:
                    print(f"Failed to send message to {chat_id}. Status code: {r.status_code}")

    else:
        print("No new links found.")

    # ---------------- UPDATE SEEN LINKS ----------------
    with open(seen_file, "w") as f:
        for link in current_links.union(seen_links):
            f.write(link + "\n")

print("Starting scraper....")
check_new_assistenze()

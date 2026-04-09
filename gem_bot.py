from playwright.sync_api import sync_playwright
import csv
import os
import re
import requests
import time

TOKEN = "8740732233:AAFuRZd2AVE_0TdcA2y0wWXu1OCJigAul3E"
CHAT_ID = "5895658222"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# Load seen bids
if os.path.exists("seen.txt"):
    with open("seen.txt", "r") as f:
        seen = set(f.read().splitlines())
else:
    seen = set()

# Load categories
categories = []
with open("Cat.csv", newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            categories.append(row[0].strip())

new_bids = []
all_bids = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for cat in categories:
        try:
            print(f"Checking: {cat}")

            page.goto(f"https://bidplus.gem.gov.in/all-bids?q={cat}", timeout=60000)
            time.sleep(5)

            html = page.content()

            found = re.findall(r"GEM/\d+/B/\d+", html)

            for bid in found:
                full = f"{bid} | {cat}"
                all_bids.add(full)

                if full not in seen:
                    new_bids.append(full)

        except Exception as e:
            print(f"Error: {e}")

    browser.close()

# Send new bids
for bid in new_bids:
    bid_id, cat = bid.split(" | ")
    send(f"🆕 New Tender\n📦 {cat}\n🆔 {bid_id}")

# Save
with open("seen.txt", "w") as f:
    for b in seen.union(all_bids):
        f.write(b + "\n")

print("Done")

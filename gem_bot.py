import requests
import csv
import os
import re
import time

TOKEN = "8740732233:AAFuRZd2AVE_0TdcA2y0wWXu1OCJigAul3E"
CHAT_ID = "5895658222"

def send_telegram(msg):
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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

for cat in categories:
    try:
        print(f"Checking: {cat}")

        url = "https://bidplus.gem.gov.in/all-bids"
        params = {"q": cat}

        res = requests.get(url, headers=headers, params=params, timeout=20)
        html = res.text

        found = re.findall(r"GEM/\d+/B/\d+", html)

        for bid in found:
            full = f"{bid} | {cat}"
            all_bids.add(full)

            if full not in seen:
                new_bids.append(full)

        time.sleep(3)

    except Exception as e:
        print(f"Error in {cat}: {e}")

# Send new bids
for bid in new_bids:
    bid_id, cat = bid.split(" | ")
    send_telegram(f"🆕 New Tender\n📦 {cat}\n🆔 {bid_id}")

# Save
with open("seen.txt", "w") as f:
    for b in seen.union(all_bids):
        f.write(b + "\n")

print("Done")

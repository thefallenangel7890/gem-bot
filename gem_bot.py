import requests
import csv
import os
import re
import time

# 🔐 Telegram Credentials
TOKEN = "8740732233:AAFuRZd2AVE_0TdcA2y0wWXu1OCJigAul3E"
CHAT_ID = "5895658222"

# 📩 Send message to Telegram
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except:
        pass

# 📂 Load already seen bids
if os.path.exists("seen.txt"):
    with open("seen.txt", "r") as f:
        seen_bids = set(f.read().splitlines())
else:
    seen_bids = set()

# 📂 Load categories from CSV
categories = []
with open("Cat.csv", newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            categories.append(row[0].strip())

# 🧠 Store new bids
new_bids = []
all_bids = set()

# 🔍 Fetch bids for each category
for category in categories:
    try:
        print(f"Checking: {category}")

        url = f"https://bidplus.gem.gov.in/all-bids?q={category}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=15)
        html = response.text

        # 🔎 Extract bid numbers
        found_bids = re.findall(r"GEM/\d+/B/\d+", html)

        for bid in found_bids:
            full_bid = f"{bid} | {category}"
            all_bids.add(full_bid)

            if full_bid not in seen_bids:
                new_bids.append(full_bid)

        time.sleep(2)  # avoid blocking

    except Exception as e:
        print(f"Error in {category}: {e}")

# 📤 Send only NEW bids
if new_bids:
    for bid in new_bids:
        try:
            bid_id, category = bid.split(" | ")

            message = f"""
🆕 New GeM Tender

📦 Category: {category}
🆔 Bid No: {bid_id}

🔗 https://bidplus.gem.gov.in/all-bids
"""
            send_telegram(message)
            time.sleep(1)

        except:
            pass
else:
    print("No new bids today.")

# 💾 Save updated bids
with open("seen.txt", "w") as f:
    for bid in seen_bids.union(all_bids):
        f.write(bid + "\n")

print("✅ Done")

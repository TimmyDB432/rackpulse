import json
import os
import re
from datetime import datetime
import feedparser

DATA_FILE = "public/data.json"

# Targeted feeds for homelab, networking, and prosumer hardware
FEEDS = [
    # Hacker News RSS filtered for homelab and server hardware
    "https://hnrss.org/newest?q=homelab+OR+mini-pc+OR+proxmox+OR+switch+OR+firewall",
]

KEYWORDS = ["homelab", "server", "switch", "router", "firewall", "nas", "mini pc", "enterprise", "ssd"]

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def scrape_feeds():
    existing_data = load_existing_data()
    existing_titles = {item["title"] for item in existing_data}
    new_items_count = 0

    for feed_url in FEEDS:
        print(f"Fetching feed: {feed_url}")
        parsed_feed = feedparser.parse(feed_url)
        
        for entry in parsed_feed.entries[:15]:
            title = entry.get("title", "Unknown Title")
            link = entry.get("link", "#")
            published = entry.get("published", datetime.utcnow().isoformat())
            summary = clean_html(entry.get("summary", "No summary available."))

            combined_text = (title + " " + summary).lower()
            if not any(kw in combined_text for kw in KEYWORDS):
                continue

            if title not in existing_titles:
                new_item = {
                    "id": f"{int(datetime.utcnow().timestamp())}-{new_items_count}",
                    "title": title,
                    "link": link,
                    "published": published,
                    "summary": summary[:250] + "...",
                    "category": "Homelab / Hardware"
                }
                existing_data.insert(0, new_item)
                existing_titles.add(title)
                new_items_count += 1

    save_data(existing_data)
    print(f"Ingestion complete. Added {new_items_count} new gear items.")

if __name__ == "__main__":
    scrape_feeds()

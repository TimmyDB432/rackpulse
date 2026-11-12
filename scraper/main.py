import os
import json
import feedparser
from datetime import datetime

# Expanded feed list including vendor releases and prosumer hardware sources
FEEDS = [
    {
        "name": "Ubiquiti Releases",
        "url": "https://community.ui.com/rss/releases/Releases/e6712595-81bb-4829-8e42-9e2630fabcfe",
        "category": "Networking / Ubiquiti"
    },
    {
        "name": "ServeTheHome",
        "url": "https://www.servethehome.com/feed/",
        "category": "Servers & Storage"
    },
    {
        "name": "Jeff Geerling",
        "url": "https://www.jeffgeerling.com/blog.xml",
        "category": "Homelab & Pi"
    },
    {
        "name": "Ars Technica Hardware",
        "url": "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "category": "Hardware"
    }
]

def scrape_feeds():
    all_items = []
    
    for feed_info in FEEDS:
        print(f"Fetching {feed_info['name']}...")
        parsed = feedparser.parse(feed_info['url'])
        
        for entry in parsed.entries:
            # Extract basic fields safely
            title = entry.get('title', 'No Title')
            link = entry.get('link', '#')
            summary = entry.get('summary', entry.get('description', 'No summary available.'))
            
            # Normalize published date
            published_parsed = entry.get('published_parsed', entry.get('updated_parsed'))
            if published_parsed:
                pub_date = datetime(*published_parsed[:6]).isoformat()
            else:
                pub_date = datetime.now().isoformat()

            all_items.append({
                "title": title,
                "link": link,
                "summary": summary,
                "published": pub_date,
                "category": feed_info['category']
            })

    # Sort items by publication date (newest first)
    all_items.sort(key=lambda x: x['published'], reverse=True)
    
    # Keep top 50 latest items to keep data.json lean
    return all_items[:50]

def save_to_json(data):
    output_path = os.path.join('public', 'data.json')
    os.makedirs('public', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved {len(data)} items to {output_path}")

if __name__ == '__main__':
    gear_data = scrape_feeds()
    save_to_json(gear_data)

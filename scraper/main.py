import os
import json
import feedparser
from datetime import datetime

FEEDS = [
    # --- HOMELAB & INFRASTRUCTURE ---
    {
        "name": "Hacker News (Homelab / Hardware)",
        "url": "https://hnrss.org/newest?q=homelab+OR+mini-pc+OR+proxmox+OR+switch+OR+firewall",
        "category": "HN Community",
        "section": "homelab"
    },
    {
        "name": "Ubiquiti Releases",
        "url": "https://community.ui.com/rss/releases/Releases/e6712595-81bb-4829-8e42-9e2630fabcfe",
        "category": "Networking / Ubiquiti",
        "section": "homelab"
    },
    {
        "name": "ServeTheHome",
        "url": "https://www.servethehome.com/feed/",
        "category": "Servers & Storage",
        "section": "homelab"
    },
    {
        "name": "Jeff Geerling",
        "url": "https://www.jeffgeerling.com/blog.xml",
        "category": "Homelab & Pi",
        "section": "homelab"
    },

    # --- SECURITY & THREAT INTEL ---
    {
        "name": "Huntress Blog",
        "url": "https://www.huntress.com/blog/rss.xml",
        "category": "Threat Intel / Huntress",
        "section": "security"
    },
    {
        "name": "CISA Advisories",
        "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "category": "Advisories / CISA",
        "section": "security"
    },
    {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
        "category": "Security News",
        "section": "security"
    },
    {
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com/feed/",
        "category": "Investigative / Krebs",
        "section": "security"
    }
]

def scrape_feeds():
    all_items = []
    
    for feed_info in FEEDS:
        print(f"Fetching {feed_info['name']}...")
        parsed = feedparser.parse(feed_info['url'])
        
        for entry in parsed.entries[:15]: # Cap per-feed to prevent one noisy feed from flooding the list
            title = entry.get('title', 'No Title')
            link = entry.get('link', '#')
            summary = entry.get('summary', entry.get('description', 'No summary available.'))
            
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
                "category": feed_info['category'],
                "section": feed_info['section']
            })

    all_items.sort(key=lambda x: x['published'], reverse=True)
    return all_items[:80] # Increased total cap to accommodate both sections

def save_to_json(data):
    output_path = os.path.join('public', 'data.json')
    os.makedirs('public', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved {len(data)} items to {output_path}")

if __name__ == '__main__':
    gear_data = scrape_feeds()
    save_to_json(gear_data)

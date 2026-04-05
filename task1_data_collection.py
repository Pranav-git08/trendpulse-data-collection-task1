import requests
import json
import time
import os
from datetime import datetime

# My category dictionary for TrendPulse
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "globals"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

my_headers = {"User-Agent": "TrendPulse/1.0"}
final_results = []

# Step 1: Getting the IDs from HackerNews
print(" Starting Task 1 Data Collection ")
print("Fetching top 500 story IDs from HackerNews  ")
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
top_ids = requests.get(top_url, headers=my_headers).json()[:500]

# Step 2: Main loop to find 25 stories for each category
for cat_name, keywords in categories.items():
    print(f"\n Searching for Category: {cat_name} ")
    found_count = 0
    
    for sid in top_ids:
        # Check if we already found 25 for this category
        if found_count >= 25:
            break
            
        try:
            # Getting story details for each ID
            item_url = "https://hacker-news.firebaseio.com/v0/item/" + str(sid) + ".json"
            data = requests.get(item_url, headers=my_headers).json()
            
            title = data.get("title", "")
            title_lower = title.lower()
            
            # Simple manual check if any keyword is in the title
            is_match = False
            for k in keywords:
                if k.lower() in title_lower:
                    is_match = True
                    break
            
            if is_match == True:
                # Adding it to our results with the 7 required fields
                final_results.append({
                    "post_id": data.get("id"),
                    "title": title,
                    "category": cat_name,
                    "score": data.get("score", 0),
                    "num_comments": data.get("descendants", 0),
                    "author": data.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                found_count = found_count + 1
                print(f"Match found! ({found_count}/25): {title[:40]}...")

        except:
            # If one fails, skip it so the script doesn't crash
            continue
            
    # Task 1 requirement: Wait 2 seconds between each category loop
    print(f"Finished {cat_name}. Total found: {found_count}")
    time.sleep(2)

# Step 3: Saving to the data folder
if not os.path.exists("data"):
    os.makedirs("data")
    print("Created 'data' folder")

# Generating filename with today's date (YYYYMMDD)
today_date = datetime.now().strftime("%Y%m%d")
filename = "data/trends_" + today_date + ".json"

# Writing the JSON file
f = open(filename, "w")
json.dump(final_results, f, indent=4)
f.close()

print("\n Task 1 Complete ")
print(f"Total stories collected: {len(final_results)}")
print(f"File saved at: {filename}")
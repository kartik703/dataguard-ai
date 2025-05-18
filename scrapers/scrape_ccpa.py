# scrapers/scrape_ccpa.py

import requests
from bs4 import BeautifulSoup
import os

OUTPUT_FILE = "data/ccpa.txt"
SOURCE_URL = "https://oag.ca.gov/privacy/ccpa"

def scrape_ccpa_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").text.strip()
        content = soup.find("div", {"class": "field-items"}).get_text(separator="\n", strip=True)
        return f"{title}\n\n{content}"
    except Exception as e:
        print(f"❌ Failed to scrape CCPA page: {e}")
        return None

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    print(f"🔍 Scraping CCPA from {SOURCE_URL}")
    text = scrape_ccpa_page(SOURCE_URL)

    if text:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ CCPA saved to {OUTPUT_FILE}")
    else:
        print("❌ Failed to extract content")

if __name__ == "__main__":
    main()

# scrapers/scrape_hipaa.py

import requests
from bs4 import BeautifulSoup
import os

OUTPUT_FILE = "data/hipaa.txt"
SOURCE_URL = "https://www.hhs.gov/hipaa/index.html"

def scrape_hipaa_page(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "HIPAA Overview"

        # Try multiple common containers
        container = (
            soup.find("main") or
            soup.find("div", {"role": "main"}) or
            soup.find("div", class_="usa-layout-docs__main") or
            soup.body
        )

        if not container:
            raise Exception("Could not find main content.")

        content = container.get_text(separator="\n", strip=True)
        return f"{title}\n\n{content}"

    except Exception as e:
        print(f"❌ Failed to scrape HIPAA page: {e}")
        return None

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    print(f"🔍 Scraping HIPAA from {SOURCE_URL}")
    text = scrape_hipaa_page(SOURCE_URL)

    if text:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ HIPAA saved to {OUTPUT_FILE}")
    else:
        print("❌ Failed to extract content")

if __name__ == "__main__":
    main()

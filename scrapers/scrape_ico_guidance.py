# scrapers/scrape_ico_guidance.py

import requests
from bs4 import BeautifulSoup
import os

ICO_URLS = [
    "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-officers/",
    "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/",
    "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-impact-assessments/",
    "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/right-of-access/"
]

OUTPUT_FILE = "data/ico_guidance.txt"

def scrape_ico_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").text.strip()
        content = soup.find("main").get_text(separator="\n", strip=True)
        return f"{title}\n\n{content}"
    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    all_text = []
    for url in ICO_URLS:
        print(f"🔍 Scraping {url}")
        page = scrape_ico_page(url)
        if page:
            all_text.append(page)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_text))

    print(f"\n✅ ICO guidance saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

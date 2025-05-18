# scrapers/scrape_uk_gdpr_static.py

import requests
from bs4 import BeautifulSoup
import os

OUTPUT_FILE = "data/uk_gdpr_articles.txt"
BASE_URL = "https://www.legislation.gov.uk/eur/2016/679/article-{}"

def fetch_article(article_number):
    url = BASE_URL.format(article_number)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find("h1")
        content_tag = soup.find("div", class_="LegContent")

        title = title_tag.get_text(strip=True) if title_tag else f"Article {article_number}"
        content = content_tag.get_text(separator="\n", strip=True) if content_tag else "No content found"

        return f"{title}\n\n{content}"

    except Exception as e:
        print(f"❌ Failed Article {article_number}: {e}")
        return None

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    all_articles = []

    for i in range(1, 100):  # 99 articles expected
        print(f"🔍 Scraping Article {i}...")
        article = fetch_article(i)
        if article:
            all_articles.append(article)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_articles))

    print(f"\n✅ UK GDPR saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

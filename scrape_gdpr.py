# scrape_gdpr.py

import requests
from bs4 import BeautifulSoup
from time import sleep

base_url = "https://gdpr-info.eu/art-{}-gdpr/"
output_file = "data/gdpr_articles.txt"

def scrape_eu_gdpr_articles(start=1, end=100):
    articles = []
    for i in range(start, end):
        try:
            url = base_url.format(i)
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1').text.strip()
            body = soup.find('div', class_='entry-content').text.strip()
            articles.append(f"{title}\n{body}")
            print(f"[✓] Scraped Article {i}")
            sleep(1)  # Be polite to the server
        except Exception as e:
            print(f"[!] Skipping Article {i}: {e}")
            continue
    return "\n\n---\n\n".join(articles)

# Save output
text = scrape_eu_gdpr_articles()
with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\n✅ Saved GDPR articles to {output_file}")

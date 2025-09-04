import requests
from bs4 import BeautifulSoup
import json
import csv
from tenacity import retry, stop_after_attempt, wait_exponential


class BookScraper:
    BASE_URL = "http://books.toscrape.com/"

    def __init__(self):
        self.session = requests.Session()

    # Retry logic (3 tries, exponential backoff: 1s, 2s, 4s)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def fetch_page(self, url):
        response = self.session.get(url, timeout=10)
        response.raise_for_status()  # Raise error if status != 200
        return response.text

    def parse_books(self, html):
        soup = BeautifulSoup(html, "html.parser")
        books = []
        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = article.select_one("p.price_color").text
            availability = article.select_one("p.instock.availability").get_text(strip=True)
            books.append({"title": title, "price": price, "availability": availability})
        return books

    def scrape(self, pages=1):
        all_books = []
        url = self.BASE_URL
        for page in range(1, pages + 1):
            page_url = f"{self.BASE_URL}catalogue/page-{page}.html" if page > 1 else url
            print(f"Scraping: {page_url}")
            html = self.fetch_page(page_url)
            books = self.parse_books(html)
            all_books.extend(books)
        return all_books

    def save_to_json(self, data, filename="books.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def save_to_csv(self, data, filename="books.csv"):
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


if __name__ == "__main__":
    scraper = BookScraper()
    books = scraper.scrape(pages=2)  # scrape 2 pages
    scraper.save_to_json(books)
    scraper.save_to_csv(books)
    print("Scraping complete! Saved to books.json and books.csv")

import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.config import SERPER_API_KEY


class SerperClient:
    BASE_URL = "https://google.serper.dev/search"

    def __init__(self):
        if not SERPER_API_KEY:
            raise ValueError("Missing SERPER_API_KEY in environment variables")
        self.headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def search(self, query):
        payload = {"q": query}
        try:
            response = requests.post(self.BASE_URL, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[Serper API Error] {e}")
            raise


if __name__ == "__main__":
    client = SerperClient()
    results = client.search("Top 10 programming languages 2025")
    print(results)

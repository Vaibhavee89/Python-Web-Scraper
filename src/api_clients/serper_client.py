try:
    from .base_client import BaseClient
except ImportError:
    from base_client import BaseClient
from ..utils.config import SERPER_API_KEY

class SerperClient(BaseClient):
    def __init__(self):
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        }
        super().__init__(base_url="https://google.serper.dev/", headers=headers)

    def search(self, query: str, num_results: int = 5):
        payload = {"q": query, "num": num_results}
        try:
            response = self.make_request("POST", "search", json=payload)
            results = [
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                }
                for item in response.get("organic", [])
            ]
            return results
        except Exception as e:
            print(f"Error during Serper search: {e}")
            return []


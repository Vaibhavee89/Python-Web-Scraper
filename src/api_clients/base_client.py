import requests
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseClient:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def make_request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()

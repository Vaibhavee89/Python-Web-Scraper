from .base_client import BaseClient
from src.utils.config import SCENARIO_API_KEY
from src.utils.logger import get_logger


class ScenarioClient(BaseClient):
    def __init__(self):
        headers = {
            "Authorization": f"Token {SCENARIO_API_KEY}",
            "Content-Type": "application/json",
        }
        super().__init__(base_url="https://api.cloud.scenario.com/v1/", headers=headers)
        self.logger = get_logger("ScenarioClient")

    def generate_image(self, prompt: str, width: int = 512, height: int = 512):
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
        }
        try:
            response = self.make_request("POST", "generate", json=payload)
            image_url = response.get("images", [{}])[0].get("url")
            if image_url:
                self.logger.info(f"Image generated successfully for prompt: {prompt}")
                return image_url
            else:
                self.logger.warning("No image URL found in response.")
                return None
        except Exception as e:
            self.logger.error(f"Error during Scenario API call: {e}")
            return None

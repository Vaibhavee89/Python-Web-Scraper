from src.api_clients.scenario_client import ScenarioClient

def test_scenario_generate():
    client = ScenarioClient()
    image_url = client.generate_image("A futuristic cyberpunk library with neon lights")
    assert image_url is None or isinstance(image_url, str)

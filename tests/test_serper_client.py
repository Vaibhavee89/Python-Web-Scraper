from src.api_clients.serper_client import SerperClient

def test_serper_search():
    client = SerperClient()
    results = client.search("Books to Scrape website")
    assert isinstance(results, list)
    if results:
        assert "title" in results[0]

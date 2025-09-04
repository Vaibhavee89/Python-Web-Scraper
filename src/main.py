from src.api_clients.serper_client import SerperClient

if __name__ == "__main__":
    client = SerperClient()
    results = client.search("Best Python libraries 2025", num_results=3)
    for r in results:
        print(r)

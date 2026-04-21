from backend_database.data_api import TrumpDataClient

def get_latest_posts(limit=5):
    client = TrumpDataClient()
    return client.get_latest_posts(limit=limit)
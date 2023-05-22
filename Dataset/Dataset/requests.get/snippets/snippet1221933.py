import requests
import forest.map_view


@staticmethod
def fetch(endpoint):
    request = requests.get(endpoint)
    data = request.json()
    return data.get('result', [])

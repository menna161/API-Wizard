import requests
from typing import Optional
from scorers import build_scorer


def corpus_info(self):
    url = f'{self.base_url}'
    try:
        r = requests.get(url)
    except Exception as e:
        print(f'Failed to request corpus information: {e}')
    return r.json()

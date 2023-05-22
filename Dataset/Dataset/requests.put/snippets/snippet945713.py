import requests
from typing import Optional
from scorers import build_scorer


def send_hypo(self, sent_id: int, hypo: str) -> None:
    url = f'{self.base_url}/hypo'
    params = {'sent_id': sent_id}
    try:
        requests.put(url, params=params, data=hypo.encode('utf-8'))
    except Exception as e:
        print(f'Failed to send a translated segment: {e}')

import requests
from typing import Optional
from scorers import build_scorer


def new_session(self):
    url = f'{self.base_url}'
    try:
        _ = requests.post(url)
    except Exception as e:
        print(f'Failed to start an evaluation session: {e}')
    print('Evaluation session started.')
    return self

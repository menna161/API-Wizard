import requests
from typing import Optional
from scorers import build_scorer


def get_scores(self):
    url = f'{self.base_url}/result'
    try:
        r = requests.get(url)
        print('Scores: {}'.format(r.json()))
        print('Evaluation session finished.')
    except Exception as e:
        print(f'Failed to end an evaluation session: {e}')

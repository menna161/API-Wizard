import requests
from typing import Optional
from scorers import build_scorer


def get_src(self, sent_id: int, extra_params: Optional[dict]=None) -> str:
    url = f'{self.base_url}/src'
    params = {'sent_id': sent_id}
    if (extra_params is not None):
        for key in extra_params.keys():
            params[key] = extra_params[key]
    try:
        r = requests.get(url, params=params)
    except Exception as e:
        print(f'Failed to request a source segment: {e}')
    return r.json()

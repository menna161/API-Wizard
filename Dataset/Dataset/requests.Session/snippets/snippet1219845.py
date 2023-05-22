from typing import Any, Dict
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger
import requests


def ask_for_superpower(service_url: str, timeout: int=3, configuration: Configuration=None, secrets: Secrets=None) -> Dict[(str, Any)]:
    '\n    Fetch a superpower\n    '
    global session
    if (not session):
        session = requests.Session()
    headers = {'Accept': 'application/json'}
    info = {}
    try:
        r = session.get(service_url, headers=headers, timeout=(timeout, timeout))
    except requests.exceptions.Timeout as x:
        logger.warning('Superpowers were too slow to arrive!')
        return False
    if (r.status_code == 200):
        info = r.json()
        fetched_superpowers.append(info)
    return {'status': r.status_code, 'headers': dict(**r.headers), 'body': info}

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from percy.user_agent import UserAgent
from percy import utils


def _requests_retry_session(self, retries=3, backoff_factor=0.3, method_whitelist=['HEAD', 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE'], status_forcelist=(500, 502, 503, 504, 520, 524), session=None):
    session = (session or requests.Session())
    retry = Retry(total=retries, read=retries, connect=retries, status=retries, method_whitelist=method_whitelist, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

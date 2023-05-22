import json
import requests
from auvsi_suas.client.exceptions import InteropError
from auvsi_suas.proto import interop_api_pb2
from concurrent.futures import ThreadPoolExecutor
from google.protobuf import json_format


def __init__(self, url, username, password, timeout=10, max_concurrent=128, max_retries=10):
    'Create a new Client and login.\n\n        Args:\n            url: Base URL of interoperability server\n                (e.g., http://localhost:8000).\n            username: Interoperability username.\n            password: Interoperability password.\n            timeout: Individual session request timeout (seconds).\n            max_concurrent: Maximum number of concurrent requests.\n            max_retries: Maximum attempts to establish a connection.\n        '
    self.url = url
    self.username = username
    self.timeout = timeout
    self.max_concurrent = 128
    self.session = requests.Session()
    self.session.mount('http://', requests.adapters.HTTPAdapter(pool_maxsize=max_concurrent, max_retries=max_retries))
    creds = interop_api_pb2.Credentials()
    creds.username = username
    creds.password = password
    self.post('/api/login', data=json_format.MessageToJson(creds))

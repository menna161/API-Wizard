import json
import requests
from auvsi_suas.client.exceptions import InteropError
from auvsi_suas.proto import interop_api_pb2
from concurrent.futures import ThreadPoolExecutor
from google.protobuf import json_format


def post(self, uri, **kwargs):
    'POST request to server.\n\n        Args:\n            uri: Server URI to access (without base URL).\n            **kwargs: Arguments to requests.Session.post method.\n        Raises:\n            InteropError: Error from server.\n            requests.Timeout: Request timeout.\n        '
    r = self.session.post((self.url + uri), timeout=self.timeout, **kwargs)
    if (not r.ok):
        raise InteropError(r)
    return r

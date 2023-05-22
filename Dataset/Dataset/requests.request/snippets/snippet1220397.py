import json
import requests
from ..exceptions import InternalError


def request(self, method, url, headers, data=None):
    if False:
        print('\n')
        print(method)
        print(headers)
        print(url)
        print(json.dumps(data))
    try:
        r = requests.request(method=method, url=url, headers=headers, data=data)
        if (r.status_code >= 400):
            raise InternalError(r.content)
        content = r.json()
        content['status_code'] = r.status_code
    except json.decoder.JSONDecodeError:
        raise InternalError
    except requests.exceptions.ConnectionError:
        raise ConnectionError
    return content

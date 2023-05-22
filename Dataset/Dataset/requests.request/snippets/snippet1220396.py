from ..exceptions import InternalError
import json
import requests


def request(self, url, query, variables=None, headers={}):
    try:
        data = {'query': query}
        if variables:
            data['variables'] = variables
        r = requests.request(method='POST', url=url, headers=headers, data=json.dumps(data))
        if (r.status_code >= 400):
            raise InternalError(r.content)
        content = r.json()
    except json.decoder.JSONDecodeError:
        raise InternalError
    except requests.exceptions.ConnectionError:
        raise ConnectionError
    return content

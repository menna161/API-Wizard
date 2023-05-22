from typing import Any
import requests


def browse(self, request: Request):
    try:
        r = requests.request(request.method, request.url, headers=request.headers, data=request.body, timeout=self.timeout)
        response = Response(r.content, r.json(), r.status_code)
    except ValueError as ve:
        response = Response(r.content, None, r.status_code)
    except Exception as e:
        response = Response(e, {}, 500)
    self.logger(request, response)
    return response

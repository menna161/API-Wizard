import requests


def table(locs, ip=DEFAULT_IP, port=DEFAULT_PORT):
    req = format_request('table', locs, ip, port)
    return requests.get(req).json()

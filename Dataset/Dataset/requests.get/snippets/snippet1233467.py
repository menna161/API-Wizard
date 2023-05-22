import requests


def route(locs, extra_args='', ip=DEFAULT_IP, port=DEFAULT_PORT):
    req = format_request('route', locs, ip, port)
    req += '?alternatives=false&steps=false&overview=full&continue_straight=false'
    req += extra_args
    return requests.get(req).json()

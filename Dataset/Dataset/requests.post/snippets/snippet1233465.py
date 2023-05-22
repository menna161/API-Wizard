import json
import requests


def table(locs, profile, ip=DEFAULT_IP, port=DEFAULT_PORT):
    url = ((((('http://' + ip) + ':') + port) + '/ors/v2/matrix/') + profile)
    req = requests.post(url, data=json.dumps({'locations': locs}), headers={'Content-type': 'application/json'})
    return req.json()

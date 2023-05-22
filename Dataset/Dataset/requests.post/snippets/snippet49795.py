from github import Github
import requests


def get_token(self, code, client_id, secret):
    data = {'client_id': client_id, 'client_secret': secret, 'code': code}
    headers = {'Accept': 'application/json'}
    r = requests.post('https://github.com/login/oauth/access_token', data=data, headers=headers)
    return r.json().get('access_token')

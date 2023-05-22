import os
import sys
from http import HTTPStatus
from typing import Optional, Tuple
import requests


def create(token, repo, body, issue_number) -> Tuple[(str, str)]:
    headers = {'Authorization': f'token {token}'}
    data = {'body': body}
    resp = requests.post(f'{GITHUB_API_BASE_URL}/repos/{repo}/issues/{issue_number}/comments', headers=headers, json=data)
    if (resp.status_code != HTTPStatus.CREATED):
        print_action_error(f'cannot create comment')
        print_action_debug(f'status code: {resp.status_code}')
        print_action_debug(f'response body: {resp.text}')
        exit(1)
    json = resp.json()
    return (str(json['id']), body)

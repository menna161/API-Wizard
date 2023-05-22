import os
import sys
from http import HTTPStatus
from typing import Optional, Tuple
import requests


def edit(token, repo, body, comment_id) -> Tuple[(str, str)]:
    headers = {'Authorization': f'token {token}'}
    data = {'body': body}
    resp = requests.patch(f'{GITHUB_API_BASE_URL}/repos/{repo}/issues/comments/{comment_id}', headers=headers, json=data)
    if (resp.status_code != HTTPStatus.OK):
        print_action_error(f'cannot edit comment')
        print_action_debug(f'status code: {resp.status_code}')
        print_action_debug(f'response body: {resp.text}')
        exit(1)
    json = resp.json()
    return (str(json['id']), body)

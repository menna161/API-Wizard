import os
import sys
from http import HTTPStatus
from typing import Optional, Tuple
import requests


def delete(token, repo, comment_id) -> Tuple[(str, str)]:
    headers = {'Authorization': f'token {token}'}
    resp = requests.delete(f'{GITHUB_API_BASE_URL}/repos/{repo}/issues/comments/{comment_id}', headers=headers)
    if (resp.status_code != HTTPStatus.NO_CONTENT):
        print_action_error(f'cannot delete comment')
        print_action_debug(f'status code: {resp.status_code}')
        print_action_debug(f'response body: {resp.text}')
        exit(1)
    return ('', '')

import logging
import json
import os
import boto3
import requests
from datetime import date, datetime


def findIdleRunner():
    token = getGitHubSecret()
    url = f"https://api.github.com/repos/{os.environ['REPO_OWNER']}/{os.environ['REPO_NAME']}/actions/runners"
    header = {'Authorization': 'token {}'.format(token)}
    response = requests.get(url, headers=header)
    jsonData = response.json()
    runners = []
    for runner in jsonData['runners']:
        if ((runner['status'] == 'online') and (runner['busy'] == False)):
            runners.append(runner['name'].split('my-runners-')[1])
    if (len(runners) == 0):
        return None
    if (len(runners) == 1):
        return runners[0]
    return getOldestInstance(runners)

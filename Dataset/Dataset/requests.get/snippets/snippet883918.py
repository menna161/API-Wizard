import logging
import json
import os
import boto3
import requests


def getQueuedWorkFlowsCount():
    token = getGitHubSecret()
    url = f"https://api.github.com/repos/{os.environ['REPO_OWNER']}/{os.environ['REPO_NAME']}/actions/runs?status=queued"
    header = {'Authorization': 'token {}'.format(token)}
    response = requests.get(url, headers=header)
    jsonData = response.json()
    return jsonData['total_count']

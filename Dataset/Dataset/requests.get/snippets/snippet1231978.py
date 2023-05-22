import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def get_latest_commit(self, project_id, branch):
    repository_id = self.get_repository_id(project_id)
    response = requests.get(LIST_COMMITS_ENDPOINT.format(host=self.host), headers=self.headers, params={'limit': 10000, 'ordering': '-commit_time'})
    response.raise_for_status()
    for commit in response.json()['results']:
        if ((commit['repository'] == repository_id) and (commit['ref'] == branch)):
            return commit['identifier']

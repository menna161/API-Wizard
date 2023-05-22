import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def get_repository_id(self, project_id):
    response = requests.get(LIST_REPOSITORIES_ENDPOINT.format(host=self.host), headers=self.headers, params={'limit': 10000})
    response.raise_for_status()
    for repository in response.json()['results']:
        if (repository['project']['id'] == project_id):
            return repository['id']

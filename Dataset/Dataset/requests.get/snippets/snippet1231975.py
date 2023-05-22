import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def get_project_id(self, project_name):
    response = requests.get(LIST_PROJECTS_ENDPOINT.format(host=self.host), headers=self.headers, params={'limit': 10000})
    response.raise_for_status()
    for project in response.json()['results']:
        if (project['name'] == project_name):
            return project['id']

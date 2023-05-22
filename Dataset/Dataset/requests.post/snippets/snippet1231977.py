import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def fetch_repository(self, project_id):
    '\n        Make Valohai fetch the latest commits.\n        '
    response = requests.post(FETCH_REPOSITORY_ENDPOINT.format(host=self.host, project_id=project_id), headers=self.headers)
    response.raise_for_status()
    return response.json()

import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def add_execution_tags(self, tags, execution_id):
    response = requests.post(SET_EXECUTION_TAGS_ENDPOINT.format(host=self.host, execution_id=execution_id), headers=self.headers, json={'tags': tags})
    response.raise_for_status()
    return response.json()

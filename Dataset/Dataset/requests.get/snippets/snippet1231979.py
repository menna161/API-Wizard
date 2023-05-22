import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def get_execution_details(self, execution_id):
    response = requests.get(GET_EXECUTION_DETAILS_ENDPOINT.format(host=self.host, execution_id=execution_id), headers=self.headers)
    response.raise_for_status()
    return response.json()

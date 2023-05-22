import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def get_output_url(self, output_id, limit=100):
    response = requests.get(GET_OUTPUT_URL.format(host=self.host, output_id=output_id), headers=self.headers)
    response.raise_for_status()
    data = response.json()
    return data['url']

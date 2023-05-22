import time
import logging
import requests
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException


def get_execution_outputs(self, execution_id, limit=100):
    response = requests.get(GET_EXECUTION_OUTPUTS_ENDPOINT.format(host=self.host, execution_id=execution_id, limit=limit), headers=self.headers)
    response.raise_for_status()
    data = response.json()
    outputs = data['results']
    next_page = data['next']
    while next_page:
        response = requests.get(next_page, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        outputs = (outputs + data['results'])
        next_page = data['next']
    return outputs

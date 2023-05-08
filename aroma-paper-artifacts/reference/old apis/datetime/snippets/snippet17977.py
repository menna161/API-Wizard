from afctl.utils import Utility
import pytest
import os, subprocess
from afctl.tests.utils import create_path_and_clean, PROJECT_NAME, PROJECT_CONFIG_DIR, clean_up


def test_generate_dag_template(self):
    project_name = 'tes_project'
    path = '/tmp'
    dag = 'test'
    Utility.generate_dag_template(project_name, dag, path)
    expected_output = " \nfrom airflow import DAG\nfrom datetime import datetime, timedelta\n\ndefault_args = {\n'owner': 'tes_project',\n# 'depends_on_past': ,\n# 'start_date': ,\n# 'email': ,\n# 'email_on_failure': ,\n# 'email_on_retry': ,\n# 'retries': 0\n\n}\n\ndag = DAG(dag_id='test', default_args=default_args, schedule_interval='@once')\n\n\n        "
    current_output = open(os.path.join('/tmp', 'test_dag.py')).read()
    expected_output = expected_output.replace(' ', '')
    current_output = current_output.replace(' ', '')
    assert (expected_output == current_output)

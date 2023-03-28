from __future__ import absolute_import, division, print_function, unicode_literals
import datetime
from airflow import DAG
import airflow_declarative
from airflow_declarative.compat import BaseOperator


def test_example_bash_operator(good_dag_path):
    path = good_dag_path('example_bash_operator')
    dags = airflow_declarative.from_path(path)
    assert (len(dags) == 1)
    yml_dag = dags[0]
    assert isinstance(yml_dag, DAG)
    assert (yml_dag.dagrun_timeout == datetime.timedelta(minutes=60))
    assert (yml_dag.default_args['owner'] == 'airflow')
    assert (yml_dag.start_date == datetime.datetime(2017, 7, 27, 0, 0, 0))
    assert (yml_dag.end_date == datetime.datetime(2018, 6, 27, 12, 0, 0))
    assert (yml_dag.schedule_interval == datetime.timedelta(days=1))
    expected_tasks = {'runme_0', 'runme_1', 'runme_2', 'also_run_this', 'run_after_loop', 'run_this_last'}
    assert (set(yml_dag.task_ids) == expected_tasks)
    run_after_loop = yml_dag.task_dict['run_after_loop']
    assert isinstance(run_after_loop, BaseOperator)
    assert (run_after_loop.bash_command == 'echo 1')
    expected_upstreams = {'runme_0', 'runme_1', 'runme_2'}
    assert (set(run_after_loop.upstream_task_ids) == expected_upstreams)
    run_this_last = yml_dag.task_dict['run_this_last']
    expected_upstreams = {'also_run_this', 'run_after_loop'}
    assert (set(run_this_last.upstream_task_ids) == expected_upstreams)
    also_run_this = yml_dag.task_dict['also_run_this']
    assert isinstance(run_after_loop, BaseOperator)
    expected_command = 'echo "run_id={{ run_id }} | dag_run={{ dag_run }}"'
    assert (also_run_this.bash_command == expected_command)

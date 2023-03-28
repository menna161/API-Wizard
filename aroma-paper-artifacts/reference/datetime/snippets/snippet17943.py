from mako.template import Template


def dag_template(name, config_name):
    template = Template("\nfrom airflow import DAG\nfrom datetime import datetime, timedelta\n\ndefault_args = {\n'owner': '${config_name}',\n# 'depends_on_past': ,\n# 'start_date': ,\n# 'email': ,\n# 'email_on_failure': ,\n# 'email_on_retry': ,\n# 'retries': 0\n\n}\n\ndag = DAG(dag_id='${name}', default_args=default_args, schedule_interval='@once')\n\n    \n")
    return template.render_unicode(name=name, config_name=config_name)

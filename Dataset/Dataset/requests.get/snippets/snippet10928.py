import requests, base64, logging, os, errno, shutil, sys, yaml
from pprint import pprint
import urllib.parse
from multiprocessing import Pool
import click
import git
from easydict import EasyDict


def dbc(endpoint, json, ignored_errors=[]):
    api_method = (requests.get if (endpoint in ['workspace/list', 'workspace/export', 'clusters/list-zones', 'clusters/spark-versions']) else requests.post)
    if os.environ.get('DBC_USER'):
        res = api_method((settings()['api_url'] + endpoint), json=json, auth=(os.environ['DBC_USER'], os.environ['DBC_PASS']))
    else:
        res = api_method((settings()['api_url'] + endpoint), json=json)
    if (res.status_code == 401):
        raise click.ClickException('Unauthorized call to Databricks (remember to create a netrc file to authenticate with DBC - and check if your user/pass is the one used for DBC)')
    if ((res.status_code == requests.codes.ok) or (res.json()['error_code'] in ignored_errors)):
        return res.json()
    else:
        raise click.ClickException(res.text)

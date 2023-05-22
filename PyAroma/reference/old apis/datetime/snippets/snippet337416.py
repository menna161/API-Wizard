from flask import Flask
from appkernel import AppKernelEngine
from datetime import datetime
from appkernel.util import OBJ_PREFIX
from .utils import User, create_and_save_some_users, create_and_save_a_user, create_and_save_john_jane_and_max, Project, Task, list_flask_routes
import os
import pytest
import simplejson as json
import json


def test_get_query_between_dates(client):
    u = User().update(name='some_user', password='some_pass')
    u.birth_date = datetime.strptime('1980-06-30', '%Y-%m-%d')
    u.description = 'some description'
    u.roles = ['User', 'Admin', 'Operator']
    user_id = u.save()
    print('\nSaved user -> {}'.format(User.find_by_id(user_id)))
    rsp = client.get('/users/?birth_date=>1980-06-30&birth_date=<1985-08-01&logic=AND')
    print('\nResponse: {} -> {}'.format(rsp.status, rsp.data.decode()))
    assert (rsp.status_code == 200), 'the status code is expected to be 200'
    result = rsp.json
    assert (result.get('_items')[0].get('id') == user_id)
    assert ('_links' in result)
    assert ('_type' in result)

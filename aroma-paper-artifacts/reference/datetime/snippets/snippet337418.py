from flask import Flask
from appkernel import AppKernelEngine
from datetime import datetime
from appkernel.util import OBJ_PREFIX
from .utils import User, create_and_save_some_users, create_and_save_a_user, create_and_save_john_jane_and_max, Project, Task, list_flask_routes
import os
import pytest
import simplejson as json
import json


def test_find_date_range(client):
    base_birth_date = datetime.strptime('1980-01-01', '%Y-%m-%d')
    for m in range(1, 13):
        u = User().update(name='multi_user_{}'.format(m)).update(password='some default password').append_to(roles=['Admin', 'User', 'Operator']).update(description='some description').update(birth_date=base_birth_date.replace(month=m))
        u.save()
    assert (User.count() == 12)
    rsp = client.get('/users/?birth_date=>1980-03-01&birth_date=<1980-05-30&logic=AND')
    print('\nResponse: {} -> {}'.format(rsp.status, rsp.data.decode()))
    response_list = rsp.json
    assert (len(response_list) == 3)

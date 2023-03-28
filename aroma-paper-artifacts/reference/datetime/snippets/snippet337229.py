import json
from decimal import Decimal
from pymongo import MongoClient
from appkernel import PropertyRequiredException
from appkernel.configuration import config
from appkernel.repository import mongo_type_converter_to_dict, mongo_type_converter_from_dict
from .utils import *
import pytest
from jsonschema import validate


def test_describe_rich_model():
    project_spec = Project.get_parameter_spec()
    print(Project.get_paramater_spec_as_json())
    assert project_spec.get('created').get('required')
    assert (project_spec.get('created').get('type') == 'datetime')
    assert project_spec.get('name').get('required')
    assert (project_spec.get('name').get('type') == 'str')
    name_validators = project_spec.get('name').get('validators')
    assert (len(name_validators) == 1)
    assert (name_validators[0].get('type') == 'NotEmpty')
    assert ((name_validators[0].get('value') is None) or 'null')
    tasks = project_spec.get('tasks')
    assert (not tasks.get('required'))
    assert ('sub_type' in tasks)
    assert (tasks.get('type') == 'list')
    task = tasks.get('sub_type')
    assert (task.get('type') == 'Task')
    assert ('props' in task)
    props = task.get('props')
    assert (not props.get('closed_date').get('required'))
    assert (props.get('closed_date').get('type') == 'datetime')
    assert (props.get('closed_date').get('validators')[0].get('type') == 'Past')

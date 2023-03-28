import json
from pymongo.errors import WriteError
import time
from appkernel.model import CustomProperty
from .utils import *
from appkernel.configuration import config
from pymongo import MongoClient
import pytest
from datetime import timedelta, date


def test_smaller_than_date():
    (john, jane, max) = create_and_save_john_jane_and_max()
    time.sleep(1)
    user_iterator = User.find((User.created < datetime.now()))
    results = [user for user in user_iterator]
    print('\n>fetched: {}'.format(len(results)))
    assert (len(results) == 3)

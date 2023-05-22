import json
from pymongo.errors import WriteError
import time
from appkernel.model import CustomProperty
from .utils import *
from appkernel.configuration import config
from pymongo import MongoClient
import pytest
from datetime import timedelta, date


def test_between_date_negative():
    (john, jane, max) = create_and_save_john_jane_and_max()
    user_iterator = User.find(((User.created > (datetime.now() - timedelta(days=2))) & (User.created < (datetime.now() - timedelta(days=1)))))
    results = [user for user in user_iterator]
    print('\n>fetched: {}'.format(len(results)))
    assert (len(results) == 0)

import json
from pymongo.errors import WriteError
import time
from appkernel.model import CustomProperty
from .utils import *
from appkernel.configuration import config
from pymongo import MongoClient
import pytest
from datetime import timedelta, date


def test_between_date():
    (john, jane, max) = create_and_save_john_jane_and_max()
    yesterday = (datetime.now() - timedelta(days=1))
    tomorrow = (datetime.now() + timedelta(days=1))
    user_iterator = User.find(((User.created > yesterday) & (User.created < tomorrow)))
    results = [user for user in user_iterator]
    print('\n>fetched: {}'.format(len(results)))
    assert (len(results) == 3)

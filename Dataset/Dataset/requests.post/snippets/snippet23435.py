from uuid import uuid4
import asyncio
import os
import pytest
import requests
from chunnel.socket import Socket


@pytest.fixture
def user_id():
    id_ = str(uuid4())
    response = requests.post('http://{}/api/users'.format(TEST_CARD_URL), json={'user': {'id': id_, 'rooms': ['lobby']}})
    assert (response.status_code == 201)
    return id_

import datetime
import random
import time
import unittest
import uuid
from pamqp import body, commands, constants, header
from aiorabbit import message


def setUp(self) -> None:
    self.delivery_tag = random.randint(0, 100000000)
    self.message_count = random.randint(0, 1000)
    self.redelivered = bool(random.randint(0, 1))
    super().setUp()

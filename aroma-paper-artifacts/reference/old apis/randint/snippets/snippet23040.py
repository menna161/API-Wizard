import datetime
import random
import time
import unittest
import uuid
from pamqp import body, commands, constants, header
from aiorabbit import message


def setUp(self) -> None:
    self.reply_code = random.randint(200, 500)
    self.reply_text = str(uuid.uuid4())
    super().setUp()

import random
import string
from collections import namedtuple
from unittest.mock import Mock


def __init__(self):
    self.history = []
    self.sendMessage = MockMethod(result={'message_id': random.randint(1, 1000)})
    self.editMessageText = MockMethod()
    self.editMessageReplyMarkup = MockMethod()
    self.getFile = MockMethod(result='https://google.com/robots.txt')

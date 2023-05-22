from __future__ import absolute_import
from builtins import object
import random
from .deal import Deal
from core.callhistory import CallHistory


@classmethod
def random(cls):
    board_number = random.randint(1, 16)
    return Board(board_number)

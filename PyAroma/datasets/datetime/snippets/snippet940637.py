import typing as T
import datetime
import inspect
import itertools
from .. import schedule as schedule_mod
from ..room import Room


def __init__(self, room: 'Room', now: datetime.datetime, env: T.Dict[(str, T.Any)]) -> None:
    self._room = room
    self._app = room.app
    self._now = now
    self._env = env

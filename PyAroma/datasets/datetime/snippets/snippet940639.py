import typing as T
import datetime
import inspect
import itertools
from .. import schedule as schedule_mod
from ..room import Room


def __init__(self, *args: T.Any, **kwargs: T.Any) -> None:
    super().__init__(*args, **kwargs)
    self.app = self._app
    self.room = self._room
    self.room_name = self._room.name
    self.datetime = datetime
    self.now = self._now
    self.date = self._now.date()
    self.time = self._now.time()
    self.schedule_snippets = self._app.cfg['schedule_snippets']

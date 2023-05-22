from functools import partial
import dbus
from dbus import PROPERTIES_IFACE
import gi
from gi.repository import TelepathyGLib
from gi.repository.TelepathyGLib import Connection
from gi.repository.TelepathyGLib import Channel
from .buddy import get_owner_instance
from .buddy import BuddyModel
from .xocolor import XoColor
from gi.repository import GObject
from gi.repository import Gio


def __activity_added_cb(self, account, room_handle, activity_id):
    if (activity_id in self._activities):
        return
    activity = ActivityModel(activity_id, room_handle)
    self._activities[activity_id] = activity

import logging
import dbus
from gi.repository import TelepathyGLib
from gi.repository.TelepathyGLib import Connection
from .xocolor import XoColor
from . import connection_watcher
from gi.repository import GObject


def get_owner_instance():
    global _owner_instance
    if (_owner_instance is None):
        _owner_instance = OwnerBuddyModel()
    return _owner_instance

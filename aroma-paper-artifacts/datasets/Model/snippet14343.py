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


def __buddy_added_cb(self, account, contact_id, nick, handle):
    self._nicks[contact_id] = nick
    if (contact_id in self._buddies):
        return
    buddy = BuddyModel(nick=nick, account=account.object_path, contact_id=contact_id, handle=handle)
    self._buddies[contact_id] = buddy

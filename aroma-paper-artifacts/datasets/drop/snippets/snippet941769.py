from dicts.utils import *
from dicts.rooms import *
from dicts.items import *
from dicts.monsters import *
import player, combat, cmd, platform, os, textwrap
from time import sleep
from random import choice
import colorama as C


def do_drop(self, arg):
    current_room = ROOMS[self.location]
    if (arg.lower() in self.inventory):
        x = ((((('You dropped ' + use_an(arg.lower())) + ' ') + HIGHLIGHT_COLOR) + arg.lower()) + WHITE)
        if (len(current_room[GROUND]) < GROUND_LIMIT):
            self.inventory.remove(arg.lower())
            current_room[GROUND].append(arg.lower())
            self.display_current_room()
            self.achieve_msg(x)
        else:
            self.display_current_room()
            self.error_msg(self.ROOM_FULL)
    elif (not arg):
        self.display_current_room()
        self.error_msg(self.NO_ITEM_GIVEN_DROP)
    elif (arg.lower() not in self.inventory):
        if (arg.lower() in ITEMS):
            self.display_current_room()
            self.error_msg(self.BAD_DROP)
        else:
            self.display_current_room()
            self.error_msg('"{}"{}'.format(arg, self.UNKNOWN_ITEM))

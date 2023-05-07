import os
import re
import gi
import requests
import json_config
from gi.repository import Gtk
from gi.repository.Gdk import Color


def input_changed(self, *args):
    email = self.login_window.email_field.get_text()
    password = self.login_window.password_field.get_text()
    result = re.match('^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$', email)
    if ((result is not None) and (password is not '')):
        self.login_window.sign_in_button.set_sensitive(True)
    else:
        self.login_window.sign_in_button.set_sensitive(False)

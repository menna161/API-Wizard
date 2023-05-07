import os
import re
import gi
import requests
import json_config
from gi.repository import Gtk
from gi.repository.Gdk import Color


def signInButtonClicked(self, *args):
    COLOR_INVALID = Color(50000, 10000, 10000)
    email = self.login_window.email_field.get_text()
    password = self.login_window.password_field.get_text()
    result = re.match('^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,4})$', email)
    if (result is None):
        self.login_window.email_field.modify_fg(Gtk.StateFlags.NORMAL, COLOR_INVALID)
        return
    else:
        self.login_window.email_field.modify_fg(Gtk.StateFlags.NORMAL, None)
    self.login_window.spinner.start()
    try:
        result = is_valid(email, password)
        if result:
            self.login_window.spinner.stop()
            self.login_window.show_successful_login_dialog()
            config['usage_mode'] = 'authenticated'
            config['login_credentials']['email'] = email
            config['login_credentials']['password'] = password
        else:
            self.login_window.spinner.stop()
            self.login_window.show_failed_login_dialog()
            config['usage_mode'] = 'anonymous'
    except ConnectionError:
        self.login_window.spinner.stop()
        self.login_window.show_connection_error_dialog()
    finally:
        self.login_window.spinner.stop()

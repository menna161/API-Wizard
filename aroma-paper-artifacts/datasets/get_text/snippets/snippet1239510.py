import os
import logging
import gi
from pathlib import Path
from gi.repository import Gtk
from .login_window import LoginWindow
from susi_config import SusiConfig
import RPi.GPIO
import snowboy


def on_stt_combobox_changed(self, combo: Gtk.ComboBox):
    selection = combo.get_active()
    if (selection == STT_DEEPSPEECH):
        susicfg.set('stt', 'deepspeech_local')
    elif (selection == STT_VOSK):
        susicfg.set('stt', 'vosk')
    elif (selection == STT_GOOGLE):
        susicfg.set('stt', 'google')
    elif (selection == STT_WATSON):
        credential_dialog = WatsonCredentialsDialog(self.config_window.window)
        response = credential_dialog.run()
        if (response == Gtk.ResponseType.OK):
            username = credential_dialog.username_field.get_text()
            password = credential_dialog.password_field.get_text()
            susicfg.set('stt', 'watson')
            susicfg.set('watson.stt.user', username)
            susicfg.set('watson.stt.pass', password)
        else:
            self.config_window.init_stt_combobox()
        credential_dialog.destroy()
    elif (selection == STT_BING):
        credential_dialog = BingCredentialDialog(self.config_window.window)
        response = credential_dialog.run()
        if (response == Gtk.ResponseType.OK):
            api_key = credential_dialog.api_key_field.get_text()
            susicfg.set('stt', 'bing')
            susicfg.set('bing.api', api_key)
        else:
            self.config_window.init_stt_combobox()
        credential_dialog.destroy()

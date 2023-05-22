import os
import logging
import gi
from pathlib import Path
from gi.repository import Gtk
from .login_window import LoginWindow
from susi_config import SusiConfig
import RPi.GPIO
import snowboy


def on_tts_combobox_changed(self, combo):
    selection = combo.get_active()
    if (selection == TTS_GOOGLE):
        susicfg.set('tts', 'google')
    elif (selection == TTS_FLITE):
        susicfg.set('tts', 'flite')
    elif (selection == TTS_WATSON):
        credential_dialog = WatsonCredentialsDialog(self.config_window.window)
        response = credential_dialog.run()
        if (response == Gtk.ResponseType.OK):
            username = credential_dialog.username_field.get_text()
            password = credential_dialog.password_field.get_text()
            susicfg.set('tts', 'watson')
            susicfg.set('watson.tts.user', username)
            susicfg.set('watson.tts.pass', password)
            susicfg.set('watson.tts.voice', 'en-US_AllisonVoice')
        else:
            self.config_window.init_tts_combobox()
        credential_dialog.destroy()

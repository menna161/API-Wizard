from __future__ import absolute_import
from re import sub
import sublime_plugin
from ..api import deviot
from ..libraries.messages import Messages
from ..libraries.thread_progress import ThreadProgress
from threading import Thread
from threading import Thread
from threading import Thread
from datetime import datetime, timedelta
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads
from sublime import ok_cancel_dialog
from ..libraries.I18n import I18n


def check_update(self):
    'Check update\n\n        Checks for platformio updates each 5 days.\n        To know what is the last version of platformio\n        pypi is checked\n        '
    installed = deviot.get_sysetting('installed', False)
    if (not installed):
        return
    from datetime import datetime, timedelta
    date_now = datetime.now()
    last_check = deviot.get_sysetting('last_check_update', False)
    try:
        last_check = datetime.strptime(last_check, '%Y-%m-%d %H:%M:%S.%f')
        if (date_now < last_check):
            return
    except TypeError:
        pass
    if ((not last_check) or (date_now > last_check)):
        last_check = (date_now + timedelta(5, 0))
        deviot.save_sysetting('last_check_update', str(last_check))
    cmd = deviot.pio_command(['--version'])
    out = deviot.run_command(cmd, env_paths=self.env_paths)
    pio_version = int(sub('\\D', '', out[1]))
    last_pio_version = self.online_pio_version()
    if (pio_version < last_pio_version):
        from sublime import ok_cancel_dialog
        from ..libraries.I18n import I18n
        translate = I18n().translate
        update = ok_cancel_dialog(translate('new_pio_update{0}{1}', last_pio_version, pio_version), translate('update_button'))
        if update:
            self.show_feedback()
            self.update_pio()

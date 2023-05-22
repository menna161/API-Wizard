from library import config
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal


def _message_template(self, param, message):
    ' Log area message HTML template '
    _time = datetime.now().strftime(self._time_form)
    return f"{_time} : <font color='{_color(param)}'>{param}</font> : {message}"

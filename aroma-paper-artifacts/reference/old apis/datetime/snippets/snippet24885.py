import os
import time
import curses
import logging
from datetime import datetime, timedelta
from contextlib import contextmanager
from .__version__ import __version__


def _draw_alerts(self):
    window = self.stdscr.derwin((self.n_rows - 22), self.n_cols, 21, 0)
    window.border()
    self.add_line(window, ' Alerts ', 0, 2, attr=self.GREEN)
    records = self.akita.message_queue
    (n_rows, n_cols) = window.getmaxyx()
    (n_rows, n_cols) = ((n_rows - 2), (n_cols - 2))
    color_map = {logging.DEBUG: self.GREEN, logging.INFO: self.CYAN, logging.WARNING: self.YELLOW, logging.ERROR: self.RED}
    start = max(0, (len(records) - n_rows))
    stop = len(records)
    for (row, i) in enumerate(range(start, stop), start=1):
        record = records[i]
        timestamp = datetime.fromtimestamp(record.created)
        text = '[{:%Y-%m-%d %H:%M:%S}] '.format(timestamp)
        self.add_line(window, text, row, 1)
        color = color_map.get(record.levelno, curses.A_NORMAL)
        text = (str(record.msg) % record.args)
        self.add_line(window, text, attr=color)

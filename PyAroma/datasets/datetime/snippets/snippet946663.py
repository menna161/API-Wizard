import os
import logging
import datetime
from Settings import LOGDATA


def log(mainwindow):
    useGUI = True
    if (mainwindow == 'file_only'):
        useGUI = False
    logging.basicConfig(level=logging.INFO)
    stdout_handler = logging.getLogger('').handlers[0]
    format = 'PyAero_%Y-%m-%d____h%H-m%M-s%S.log'
    logfile = os.path.join(LOGDATA, datetime.datetime.now().strftime(format))
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    if useGUI:
        gui_handler = GuiHandler(parent=mainwindow)
        gui_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    if useGUI:
        gui_formatter = logging.Formatter('%(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    if useGUI:
        gui_handler.setFormatter(gui_formatter)
    logging.getLogger('').addHandler(file_handler)
    logging.getLogger('').addHandler(console_handler)
    if useGUI:
        logging.getLogger('').addHandler(gui_handler)
    logging.getLogger('').removeHandler(stdout_handler)
    logger = logging.getLogger(__name__)
    logger.info('Starting to log')

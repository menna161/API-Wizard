import builtins
from os import path, chdir
from configparser import ConfigParser
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPersistentModelIndex
from PyQt5.QtWidgets import QMessageBox, QWidget, QProgressBar
from gettext import gettext as _


def table_row_delete(table_widget):
    if table_widget.selectionModel().hasSelection():
        index = [QPersistentModelIndex(index) for index in table_widget.selectionModel().selectedRows()]
        if (not index):
            alert_box(_('Warning'), _('Please select entire row!'), 2)
            return
        for row in index:
            table_widget.removeRow(row.row())
    else:
        alert_box(_('Warning'), _('No configuration row selected!'), 2)

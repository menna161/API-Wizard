import os
import string
from PyQt5.QtCore import QTextCodec, QRegularExpression, Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFileDialog, QTreeWidgetItem
from deen.gui.widgets.hex import HexViewWidget
from deen.gui.widgets.text import TextViewWidget
from deen.gui.widgets.formatted import FormattedViewWidget
from deen.gui.widgets.ui_deenencoderwidget import Ui_DeenEncoderWidget
from deen import logger
from OpenSSL import crypto


def clear_content(self, widget=None):
    'Clear the content of widget. If widget\n        is not set, clear the content of the current\n        widget. This will also remove all widgets\n        that follow widget.'
    widget = (widget or self)
    self.clear_error_message(widget=widget)
    self.clear_search_highlight(widget=widget)
    if (self.parent.widgets[0] == widget):
        widget.text_field.clear()
        widget.hex_field.content = bytearray()
        widget._content = bytearray()
        widget.update_length_field()
        widget.set_field_focus()
        widget.plugin = None
        widget.ui.plugin_tree_view.selectionModel().clearSelection()
    else:
        self.previous.current_combo = None
        self.previous.set_field_focus()
        self.previous.plugin = None
        self.previous.ui.plugin_tree_view.selectionModel().clearSelection()
    self.remove_next_widgets(widget=widget)

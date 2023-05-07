import codecs
import string
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QFont, QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QPlainTextEdit, QFrame


def __init__(self, content=None, max_bytes_per_line=16, width=1, read_only=False, parent=None):
    super(HexViewWidget, self).__init__(parent)
    self.parent = parent
    self._max_bytes_per_line = max_bytes_per_line
    self._bytes_per_line = max_bytes_per_line
    self._width = width
    self._read_only = read_only
    self.setShowGrid(False)
    header = self.horizontalHeader()
    header.setMinimumSectionSize(15)
    header.setDefaultSectionSize(15)
    self.selectionModel().selectionChanged.connect(self.selection_changed)
    self.ascii_font = QFont()
    self.ascii_font.setLetterSpacing(QFont.AbsoluteSpacing, 4)
    self.bold_font = QFont()
    self.bold_font.setBold(True)
    self.current_selection = []
    self.horizontalHeader().setStretchLastSection(True)
    if content:
        self.content = content
    else:
        self.content = bytearray()

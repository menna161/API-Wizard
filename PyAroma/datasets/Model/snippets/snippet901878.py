from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QBoxLayout, QShortcut, QDialog, QCompleter
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QStringListModel, Qt
import deen.constants
from deen.gui.widgets.log import DeenLogger, DeenStatusConsole
from deen.gui.widgets.ui_deenmainwindow import Ui_MainWindow
from deen.gui.encoder import DeenEncoderWidget
from deen.gui.widgets.ui_deenfuzzysearch import Ui_DeenFuzzySearchWidget
from deen import logger


def fuzzy_search_action(self):
    'Open a dialog for quick access to actions\n        with fuzzy search.'
    focussed_widget = QApplication.focusWidget()
    self.fuzzy_search_ui.ui.fuzzy_search_field.setFocus()

    def get_data(model):
        plugins = [x[1].name for x in self.plugins.available_plugins]
        for p in ((self.plugins.codecs + self.plugins.compressions) + self.plugins.assemblies):
            plugins.append(('-' + p[1].name))
            plugins.extend([('-' + x) for x in p[1].aliases])
        for p in self.plugins.available_plugins:
            plugins.extend(p[1].aliases)
        model.setStringList(plugins)
    completer = QCompleter()
    self.fuzzy_search_ui.ui.fuzzy_search_field.setCompleter(completer)
    model = QStringListModel()
    completer.setModel(model)
    get_data(model)
    if (self.fuzzy_search_ui.exec_() == 0):
        return
    search_data = self.fuzzy_search_ui.ui.fuzzy_search_field.text()
    parent_encoder = self.get_parent_encoder(focussed_widget)
    if parent_encoder:
        parent_encoder.action_fuzzy(search_data)
    else:
        LOGGER.error(('Unable to find parent encoder for ' + str(focussed_widget)))

import os
import numpy as np
from PySide6 import QtGui, QtCore, QtWidgets
import PyAero
import Airfoil
import FileDialog
import FileSystem
import SvpMethod
import SplineRefine
import TrailingEdge
import Meshing
import ContourAnalysis as ca
from Settings import ICONS_L
import logging


def itemFileSystem(self):
    self.item_fs = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    self.item_fs.setLayout(layout)
    filesystem_model = FileSystem.FileSystemModel()
    root_path = filesystem_model.rootPath()
    self.tree = QtWidgets.QTreeView()
    self.tree.setModel(filesystem_model)
    self.tree.setRootIndex(filesystem_model.index(root_path))
    self.tree.setAnimated(True)
    self.tree.setColumnHidden(1, True)
    self.tree.setColumnHidden(2, True)
    self.tree.setColumnHidden(3, True)
    header = self.tree.header()
    header.hide()
    self.tree.clicked.connect(filesystem_model.onFileSelected)
    self.tree.doubleClicked.connect(filesystem_model.onFileLoad)
    layout.addWidget(self.tree, stretch=12)
    self.header = QtWidgets.QLabel('Loaded airfoil(s)')
    self.header.setEnabled(False)
    layout.addStretch(stretch=2)
    layout.addWidget(self.header)
    self.listwidget = ListWidget(self.parent)
    self.listwidget.setEnabled(False)
    self.listwidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    layout.addWidget(self.listwidget, stretch=5)
    layout.addStretch(stretch=1)

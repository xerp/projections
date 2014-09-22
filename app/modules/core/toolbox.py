from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from functools import partial

import app.resources.modules.core.toolbox as ui_resource

class Toolbox(QtGui.QDockWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.__widget = ui_resource.Ui_dockProjectionsTools()
        self.__widget.setupUi(self)
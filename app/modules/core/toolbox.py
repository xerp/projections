from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.core.toolbox as ui_resource
import app.modules.utils as utils

class ToolBox(QtGui.QDockWidget,utils.AbstractModule):

    def __init__(self):
        utils.AbstractModule.__init__(self,QtGui.QDockWidget,ui_resource.Ui_dockProjectionsTools())

    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

        self.in_live = False
        self.direct_live = False

    def config_components(self):
        self._widget.cmdColorScreen.setText('{0} (F9)'.format(self.config.get('LIVE', 'DEFAULT_COLOR').upper()))
        self._widget.cmdColorScreen.setShortcut('F9')
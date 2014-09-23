from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.core.statusbar as ui_resource
import app.modules.utils as utils

class StatusBar(utils.AbstractModule):

    def __init__(self):
        utils.AbstractModule.__init__(self,None,ui_resource.Ui_statusBar())
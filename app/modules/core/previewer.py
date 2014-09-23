from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.modules.utils as utils

class Previewer(QtGui.QTextEdit,utils.AbstractModule):

    def __init__(self):
        utils.AbstractModule.__init__(self,QtGui.QTextEdit)

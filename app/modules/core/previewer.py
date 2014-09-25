from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.modules.utils as utils
from app.lib.helpers import get_projections_font

class Previewer(QtGui.QTextEdit,utils.AbstractModule):

    def __init__(self,parent):
        utils.AbstractModule.__init__(self,parent,QtGui.QTextEdit)

    def config_components(self):
        self.setFont(get_projections_font(dict(self.config.items('FONT_PREVIEW'))))

    def set_text(self,text):
        self.setText(text)

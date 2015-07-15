from PyQt4 import QtGui

import app.modules.utils as utils
from app.lib.helpers import get_projections_font, to_unicode


class Previewer(QtGui.QTextEdit, utils.AbstractModule):
    def __init__(self, parent):
        utils.AbstractModule.__init__(self, parent, QtGui.QTextEdit)

    def config_components(self):
        self.setFont(get_projections_font(dict(self.config.items('FONT_PREVIEW'))))
        self.setReadOnly(True)

    def set_text(self, text):
        self.setText(text if isinstance(text, unicode) else to_unicode(text))

    def reset(self):
        self.set_text('')
        self.setVisible(True)
        self.setEnabled(True)

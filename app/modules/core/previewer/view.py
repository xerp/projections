"""Previewer view module."""

from PyQt4 import QtGui

from libraries.modules import CoreModule
from libraries.encoding import to_unicode
# from libraries.ui import get_projection_font


class Previewer(QtGui.QTextEdit, CoreModule):
    """Previewer core module."""

    def __init__(self, parent):
        """Module constructor."""
        super(Previewer, self).__init__(parent, QtGui.QTextEdit)

    def _configure(self):
        # self.setFont(get_projection_font(dict(self.config.items(
        #   'FONT_PREVIEW')), self.config.getint('LIVE', 'DEFAULT_FONT_SIZE')))
        self.setReadOnly(True)

    def set_text(self, text):
        """Set previewer text."""
        self.setText(text if isinstance(text, unicode) else to_unicode(text))

    def reset(self):
        """Reset previewer text."""
        self.set_text('')
        self.setVisible(True)
        self.setEnabled(True)

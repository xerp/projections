from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from helpers import set_alignment


class SongBody(QtGui.QTextEdit):
    def __init__(self, parent):
        super(SongBody, self).__init__(parent)

    def keyPressEvent(self, event):
        super(SongBody, self).keyPressEvent(event)

        if event.matches(QtGui.QKeySequence.Paste):
            set_alignment(self, Qt.AlignCenter)
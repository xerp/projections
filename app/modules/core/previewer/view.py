"""Previewer view module."""

from PyQt4 import QtGui

from app.libraries.modules import CoreModule, SingletonModule
from models import PreviewerModel


@SingletonModule
class Previewer(QtGui.QTextEdit, CoreModule):
    """Previewer core module."""

    def __init__(self, parent):
        """Module constructor."""
        super(CoreModule, self).__init__(parent, QtGui.QTextEdit)

    def _instance_variable(self):
        self.__model = PreviewerModel(self)

    def _configure(self):
        self.__model.configure_module()
        self.setReadOnly(True)

    def set_text(self, text):
        """Set previewer text."""
        self.__model.set_text(text)

    def reset(self):
        """Reset previewer text."""
        self.__model.reset()

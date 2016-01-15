"""Previewer view module."""

from PyQt4 import QtGui

from app.libraries.modules import CoreModule, SingletonCoreModule
from models import PreviewerModel


@SingletonCoreModule
class Previewer(QtGui.QTextEdit, CoreModule):
    """Previewer core module."""

    def __init__(self, parent):
        """Module constructor."""
        super(CoreModule, self).__init__(
            parent, PreviewerModel, QtGui.QTextEdit)

    def _configure(self):
        self._model.configure_module()
        self.setReadOnly(True)

    def set_text(self, text):
        """Set previewer text."""
        self._model.set_text(text)

    def reset(self):
        """Reset previewer text."""
        self._model.reset()

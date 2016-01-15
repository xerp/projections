"""Live viewer view module."""


from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView

from app.libraries.modules import CoreModule, SingletonCoreModule
from models import LiveViewerModel


@SingletonCoreModule
class LiveViewer(QtGui.QFrame, CoreModule):
    """LiveViewer class."""

    def __init__(self, parent):
        """LiveViewer constructor."""
        super(CoreModule, self).__init__(parent, LiveViewerModel, QtGui.QFrame)

    def _instance_variable(self):
        super(CoreModule, self)._instance_variable()

        self.__default_size = QtCore.QSize(400, 400)

        self.__main_layout = QtGui.QGridLayout(self)
        self.__lblLive = QWebView()

    def _configure(self):
        self.__model.configure_module()

    def set_visible(self, visible, screen=1):
        """Set live viewer visible."""
        self.__model.set_visible(visible, screen)

    def reset(self):
        """Reset live viewer module."""
        self.__model.reset(self.__default_size)

    def set_full_screen(self, full_screen):
        """Set full screen."""
        self.__model.set_full_screen(full_screen, self.__default_size)

    def set_color(self, color=None):
        """Set live viewer color."""
        self.__model.set_color(color, self.__lblLive)

    def set_image(self, image_file):
        """Set an image."""
        self.__model.set_image(image_file, self.__lblLive)

    def set_text(self, **kwargs):
        """Set the text to view."""
        self.__model.set_text(self.__lblLive, **kwargs)

    def set_url(self, **kwargs):
        """Set a URL to view."""
        self.__model.set_url(self.__lblLive, **kwargs)

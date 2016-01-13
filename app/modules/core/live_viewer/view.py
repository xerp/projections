"""Live viewer view module."""


from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView, QWebSettings

from app.libraries.modules import CoreModule, SingletonModule
from models import LiveViewerModel


@SingletonModule
class LiveViewer(QtGui.QFrame, CoreModule):
    """LiveViewer class."""

    def __init__(self, parent):
        """LiveViewer constructor."""
        super(CoreModule, self).__init__(parent, QtGui.QFrame)

    def _instance_variable(self):
        super(CoreModule, self)._instance_variable()

        self.__model = LiveViewerModel(self)
        self.__default_size = QtCore.QSize(400, 400)

        self.__main_layout = QtGui.QGridLayout(self)
        self.__lblLive = QWebView()

    def _configure(self):
        self.setWindowTitle('{0} Live Window'.format("hola"))
        # self.config.get('GENERAL', 'TITLE')

        self.setWindowFlags(
            Qt.CustomizeWindowHint or Qt.WindowStaysOnTopHint)
        self.setSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.__lblLive.settings().setAttribute(
            QWebSettings.LocalContentCanAccessRemoteUrls, True)

        self.__lblLive.settings().setAttribute(
            QWebSettings.LocalContentCanAccessFileUrls, True)

        self.__lblLive.settings().setAttribute(
            QWebSettings.PluginsEnabled, True)

        self.__main_layout.addWidget(self.__lblLive)
        self.__lblLive.setVisible(True)

        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.reset()

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

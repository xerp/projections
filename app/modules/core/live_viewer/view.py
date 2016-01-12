"""Live viewer view module."""

import utils

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtWebKit import QWebView, QWebSettings
from jinja2 import Template

from libraries.modules import CoreModule
from libraries.encoding import get_default_encoding
from libraries.utils import ProjectionError


class LiveViewer(QtGui.QFrame, CoreModule):
    """LiveViewer class."""

    def __init__(self, parent):
        """LiveViewer constructor."""
        super(LiveViewer, self).__init__(parent, QtGui.QFrame)

    def _instance_variable(self):
        super(LiveViewer, self)._instance_variable()

        self.size = QtCore.QSize(400, 400)

        self.__main_layout = QtGui.QGridLayout(self)
        self.__lblLive = QWebView()

    def _configure(self):

        # self.setWindowTitle('{0} Live Window'.format(
        #     self.config.get('GENERAL', 'TITLE')))

        self.setWindowFlags(Qt.CustomizeWindowHint or Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

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

    def __set_html_text(self):
        self.__lblLive.load(QUrl.fromLocalFile(utils.get_viewer_file_path()))

    def set_visible(self, visible, screen=1):
        """Set live viewer visible."""
        self.__screen_geometry = utils.get_screen_geometry(screen)

        geometry = self.geometry()
        geometry.setX(self.__screen_geometry.x())
        geometry.setY(self.__screen_geometry.y())
        self.setGeometry(geometry)

        self.reset()
        self.show() if visible else self.hide()
        self.setFixedSize(self.__screen_geometry.size())

    def reset(self):
        """Reset live viewer module."""
        self.set_full_screen(False)
        self.setFixedSize(self.size)

    def set_full_screen(self, full_screen):
        """Set full screen."""
        try:
            self.setFixedSize(self.__screen_geometry.size()
                              if full_screen else self.size)
        except Exception:
            raise ProjectionError('window must be visible before full_screen')

    def set_color(self, color=None):
        """Set live viewer color."""
        color = self.config.get(
            'LIVE', 'DEFAULT_COLOR') if not color else color

        template = Template('<body style="background-color:{{color}}"></body>')
        self.__lblLive.setHtml(template.render(color=color))

    def set_image(self, image_file):
        """Set an image."""
        self.set_color()

        if not image_file:
            raise ProjectionError('error occurred trying to loading image')

        template = Template(utils.get_image_html_view())
        utils.create_html_file(template.render(image=image_file))
        self.__set_html_text()

    def set_text(self, **kwargs):
        """Set the text to view."""
        self.set_color()

        unicode_last_template = Template(kwargs['item'])
        font_size = kwargs['font_size']
        unicode_html_text = unicode_last_template.render(
            charset=get_default_encoding,
            font_size=font_size if font_size > 0 else utils.ZOOM_OUT_STEP)

        utils.create_viewer_file(unicode_html_text)
        self.__set_html_text()

    def set_url(self, **kwargs):
        """Set a URL to view."""
        if kwargs['item']:
            self.__lblLive.load(QUrl(kwargs['item']))

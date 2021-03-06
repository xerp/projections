import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtWebKit import QWebView, QWebSettings
from jinja2 import Template

import app.modules.utils as utils
from app.lib.helpers import get_user_app_directory, to_unicode, to_str, get_default_encoding


ZOOM_OUT_STEP = 8


class LiveViewer(QtGui.QFrame, utils.AbstractModule):
    def __init__(self, parent):
        utils.AbstractModule.__init__(self, parent, QtGui.QFrame)


    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

        self.filePath = os.path.join(get_user_app_directory(), 'last_live.html')
        self.size = QtCore.QSize(400, 400)
        self.screen_geometry = None

        self.main_layout = QtGui.QGridLayout(self)
        self.lblLive = QWebView()

    def config_components(self):

        self.setWindowTitle('{0} Live Window (beta)'.format(self.config.get('GENERAL', 'TITLE')))
        self.setWindowFlags(Qt.CustomizeWindowHint or Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.lblLive.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.lblLive.settings().setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        self.lblLive.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.main_layout.addWidget(self.lblLive)
        self.lblLive.setVisible(True)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.reset()

    def __create_html_file(self, unicode_html):

        file = open(self.filePath, "w")
        file.write(to_str(unicode_html, 'latin1'))
        file.close()

    def __set_html_text(self):
        self.lblLive.load(QUrl.fromLocalFile(self.filePath))

    def set_visible(self, visible, screen=1):
        app = QtGui.QApplication.instance()

        self.screen_geometry = app.desktop().screenGeometry(screen)

        geometry = self.geometry()
        geometry.setX(self.screen_geometry.x())
        geometry.setY(self.screen_geometry.y())
        self.setGeometry(geometry)

        self.reset()
        self.show() if visible else self.hide()
        self.setFixedSize(self.screen_geometry.size())

    def reset(self):
        self.set_full_screen(False)
        self.setFixedSize(self.size)


    def set_full_screen(self, full_screen):
        try:
            self.setFixedSize(self.screen_geometry.size() if full_screen else self.size)
        except Exception:
            raise utils.ProjectionError('window must be visible before full_screen')

    def set_color(self, color=None):

        color = self.config.get('LIVE', 'DEFAULT_COLOR') if not color else color

        template = Template('<body style="background-color:{{color}}"></body>')
        self.lblLive.setHtml(template.render(color=color))

    def set_image(self, image_file):
        self.set_color()

        if not image_file:
            raise utils.ProjectionError('error occurred trying to loading image')

        html = '''
        <body>
            <style>
                body{
                    background-color:black;
                }
                img{
                    background: no-repeat;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    vertical-align: middle;
                    width:98%;
                    height:98%;
                }
            </style>
            <img src="{{image}}">
        </body>
        '''

        template = Template(html)
        self.__create_html_file(template.render(image=image_file))
        self.__set_html_text()

    def set_text(self, **kwargs):
        self.set_color()

        unicode_last_template = Template(kwargs['item'])
        font_size = kwargs['font_size']
        unicode_html_text = unicode_last_template.render(charset=get_default_encoding,
                                                         font_size=font_size if font_size > 0 else ZOOM_OUT_STEP)

        self.__create_html_file(unicode_html_text)
        self.__set_html_text()

    def set_url(self, **kwargs):
        if kwargs['item']:
            self.lblLive.load(QUrl(kwargs['item']))

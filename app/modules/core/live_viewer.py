from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtWebKit import QWebView,QWebSettings

import app.modules.utils as utils
from app.lib.helpers import get_projections_font
from jinja2 import Template


class LiveViewer(QtGui.QFrame,utils.AbstractModule):
    size = QtCore.QSize(400, 400)
    screen_geometry = None

    def __init__(self, parent):
        utils.AbstractModule.__init__(self,parent,QtGui.QFrame)


    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

        self.main_layout = QtGui.QGridLayout(self)
        self.image = QtGui.QLabel()
        self.lblLive = QWebView()

    def config_components(self):

        self.setWindowTitle('{0} Live Window (beta)'.format(self.config.get('GENERAL', 'TITLE')))
        self.setWindowFlags(Qt.CustomizeWindowHint or Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.lblLive.setVisible(True)

        self.main_layout.addWidget(self.lblLive)
        self.lblLive.page().settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls,True)
        self.lblLive.page().settings().setAttribute(QWebSettings.LocalContentCanAccessFileUrls,True)

        self.image.setScaledContents(False)

        self.reset()

    def set_visible(self, visible, screen=1):
        app = QtGui.QApplication.instance()

        self.screen_geometry = app.desktop().screenGeometry(screen)

        geometry = self.geometry()
        geometry.setX(self.screen_geometry.x())
        geometry.setY(self.screen_geometry.y())
        self.setGeometry(geometry)

        self.reset()
        self.show() if visible else self.hide()

    def reset(self):
        self.set_full_screen(False)
        self.setFixedSize(self.size)

    def __add_child(self, child):
        child.setVisible(True)
        self.main_layout.addWidget(child)

    def __remove_children(self):
        widgets = ['image', 'lblLive']

        for widget in widgets:
            obj = getattr(self, widget)

            obj.setVisible(False)
            self.main_layout.removeWidget(obj)

    def __set_html_text(self,path):
        self.lblLive.load(QUrl.fromLocalFile(path))

    def set_full_screen(self, full_screen):
        try:
            self.setFixedSize(self.screen_geometry.size() if full_screen else self.size)
        except Exception:
            raise utils.ProjectionError('window must be visible before full_screen')

    def set_color(self, color=None):

        color = QtGui.QColor(self.config.get('LIVE', 'DEFAULT_COLOR')) if not color else color

        self.__remove_children()

        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def set_image(self, image_file):
        self.set_color()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        if not image_file:
            raise utils.ProjectionError('error occurred trying to loading image')

        image = QtGui.QImage()
        image.load(image_file)

        if image.isNull():
            raise utils.ProjectionError(
                'image view not found [ path:{image} ]'.format(image=image_file[:20]))

        image = image.scaled(self.screen_geometry.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image.setPixmap(QtGui.QPixmap.fromImage(image))
        self.image.setAlignment(Qt.AlignCenter)

        self.__add_child(self.image)

    def set_text(self, html, font_size,encode='utf-8'):
        self.set_color()
        self.main_layout.setContentsMargins(0,0,0,0)
        
        self.__add_child(self.lblLive)

        self.lastEncode = encode
        self.lastTemplate = Template(html)
        self.set_font_size(font_size)


        #FIXME
        #if self.lblLive.page().currentFrame().scrollBarMaximum(Qt.Vertical) > 0:
         #   self.set_text(html,font_size - 10)

    def set_font_size(self,font_size):

        filePath = "{0}/last_live.html".format(self.config.get('GENERAL','template_path'))

        file = open(filePath, "w")
        file.write(
            self.lastTemplate.render(
                charset=self.lastEncode,
                font_size=font_size if font_size > 0 else 10).encode(self.lastEncode))
        file.close()

        self.__set_html_text(filePath)
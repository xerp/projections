from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.modules.utils as utils

class FullScreenWindow(utils.AbstractModule,QtGui.QFrame):
    size = QtCore.QSize(400, 400)
    screen_geometry = None

    def __init__(self, parent):
        QtGui.QFrame.__init__(self)
        self.parent = parent

        self.init_objects()
        self.init_component()

    def init_objects(self):
        self.main_layout = QtGui.QGridLayout(self)
        self.image = QtGui.QLabel()
        self.lblLive = QtGui.QTextEdit(self)

    def init_component(self):
        self.setWindowTitle('{0} Live Window (beta)'.format(conf.get('GENERAL', 'TITLE')))
        self.setWindowFlags(Qt.CustomizeWindowHint or Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.lblLive.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)

        self.lblLive.setReadOnly(True)
        self.lblLive.setVisible(True)

        self.main_layout.addWidget(self.lblLive)

        self.image.setScaledContents(False)

        self.reset()

    def closeEvent(self, e):
        self.parent.set_in_live(False)

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

    def set_full_screen(self, full_screen):
        try:
            self.setFixedSize(self.screen_geometry.size() if full_screen else self.size)
        except Exception:
            raise ProjectionError('window must be visible before full_screen')

    def set_color(self, color=QtGui.QColor(conf.get('LIVE', 'DEFAULT_COLOR'))):
        self.__remove_children()

        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def set_image(self, image_file):
        self.set_color()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        if not image_file:
            raise ProjectionError('error occurred trying to loading image')

        image = QtGui.QImage()
        image.load(image_file)

        if image.isNull():
            raise ProjectionError(
                'image view not found [ path:{image} ]'.format(image=image_file[:20]))

        image = image.scaled(self.screen_geometry.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image.setPixmap(QtGui.QPixmap.fromImage(image))
        self.image.setAlignment(Qt.AlignCenter)

        self.__add_child(self.image)

    def set_text(self, text, font_size=None,
                 text_color=conf.get('LIVE', 'DEFAULT_TEXT_COLOR'),
                 background_color=conf.get('LIVE', 'DEFAULT_BACKGROUND_COLOR'),
                 justification=Qt.AlignCenter):
        self.set_color()

        palette = self.lblLive.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(background_color))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(text_color))
        self.lblLive.setPalette(palette)

        text_live_margin = dict(conf.items('TEXT_LIVE_MARGIN'))
        self.main_layout.setContentsMargins(float(text_live_margin['left']), float(text_live_margin['top']),
                                            float(text_live_margin['right']), float(text_live_margin['bottom']))

        font = get_projections_font(dict(conf.items('FONT_LIVE')))

        if font_size:
            font.setPointSize(font_size)

        self.lblLive.setCurrentFont(font)
        self.lblLive.setText(text)

        set_alignment(self.lblLive, justification)

        self.__add_child(self.lblLive)

        if self.lblLive.verticalScrollBar().isVisible():
            self.set_text(text, font_size - 2, text_color, background_color, justification)
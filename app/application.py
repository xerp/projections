"""Main Application module."""

import sys
# import os

# from ConfigParser import ConfigParser

from PyQt4 import QtGui

from libraries.utils import remove_pycs
from libraries.configuration import check_user_database, get_application_geometry, set_application_geometry

from modules.core import core_modules


def main():
    """Main function call."""
    app = QtGui.QApplication(sys.argv)
    frame = Application()
    frame.show()
    remove_pycs('.')
    sys.exit(app.exec_())


class Application(QtGui.QFrame):
    """Main Application class."""

    def __init__(self):
        """Main Application Constructor."""
        QtGui.QFrame.__init__(self)

        # FIXME self.config = get_app_config()

        check_user_database()
        self.add_core_modules()
        self.window_config()
        self.configure_core_modules()

    def add_core_modules(self):
        """Add core module to main application."""
        vBoxMainLayout = QtGui.QVBoxLayout()

        # ToolBox
        self.__toolbox = core_modules.get_toolbox(self)
        vBoxMainLayout.addWidget(self.__toolbox)

        # Splitter
        splitter = QtGui.QSplitter(self)

        # Previewer
        self.__previewer = core_modules.get_previewer(self)
        splitter.addWidget(self.__previewer)

        # Controls
        # self.__controls = core_modules.get_controls(self)
        # splitter.addWidget(self.__controls)

        splitter.setSizes([700, 400])
        vBoxMainLayout.addWidget(splitter)

        # StatusBar
        self.__statusbar = core_modules.get_status_bar(self)
        vBoxMainLayout.addWidget(self.__statusbar)

        # LiveViewer
        self.__liveViewer = core_modules.get_live_viewer(self)

        self.setLayout(vBoxMainLayout)

    def window_config(self):
        """Window configuration."""
        self.setWindowTitle("{0} Manager".format("Main"))
        # self.config.get('GENERAL', 'TITLE')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/main/icons/video-projector.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        app_geometry = get_application_geometry()
        self.setGeometry(app_geometry['x'], app_geometry['y'], app_geometry[
                         'width'], app_geometry['height'])

        self.__statusbar.set_status('Ready')

    def configure_core_modules(self):
        """Configure core module."""
        # self.__controls.configure()
        self.__toolbox.configure_selected_module()

    # Handlers
    def closeEvent(self, e):
        """Close event."""
        self.__liveViewer.set_visible(False)
        self.__liveViewer.hide()

    def keyPressEvent(self, e):
        """On key press event."""
        self.__toolbox.keyPressEvent(e)
        self.__statusbar.keyPressEvent(e)
        self.__controls.keyPressEvent(e)

    def resizeEvent(self, resizeEvent):
        """On resize event."""
        set_application_geometry(self.geometry())

    def moveEvent(self, moveEvent):
        """On move event."""
        set_application_geometry(self.geometry())

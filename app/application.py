import sys

from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from modules.core import toolbox, statusbar, previewer, controls, live_viewer
from lib.helpers import remove_pycs


def main():
    app = QtGui.QApplication(sys.argv)
    frame = Application()
    frame.show()
    remove_pycs()
    sys.exit(app.exec_())


class Application(QtGui.QFrame):

    def __init__(self):
        QtGui.QFrame.__init__(self)

        self.config = ConfigParser()
        self.config.read('config.ini')

        self.add_core_modules()
        self.window_config()
        self.config_core_modules()


    def add_core_modules(self):
        vBoxMainLayout = QtGui.QVBoxLayout()
        
        #ToolBox
        self.__toolbox = toolbox.ToolBox(self)
        vBoxMainLayout.addWidget(self.__toolbox)

        #Splitter
        splitter = QtGui.QSplitter(self)

        #Previewer
        self.__previewer = previewer.Previewer(self)
        splitter.addWidget(self.__previewer)

        #Controls
        self.__controls = controls.Controls(self)
        splitter.addWidget(self.__controls)

        splitter.setSizes([700,400])
        vBoxMainLayout.addWidget(splitter)
        
        #StatusBar
        self.__statusbar = statusbar.StatusBar(self)
        vBoxMainLayout.addWidget(self.__statusbar)

        #LiveViewer
        self.__liveViewer = live_viewer.LiveViewer(self)
        
        self.setLayout(vBoxMainLayout)

    def window_config(self):

        self.setWindowTitle("{0} Manager (beta)".format(self.config.get('GENERAL', 'TITLE')))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main/icons/video-projector.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.resize(900,600)

        self.__statusbar.set_status('Ready')

    def config_core_modules(self):

        #Configure Toolbox
        self.__toolbox.set_dependents({
            'controls':self.__controls,
            'statusbar':self.__statusbar,
            'liveViewer':self.__liveViewer
            })

        #Configure Controls
        self.__controls.set_dependents({
            'toolbox':self.__toolbox,
            'statusbar':self.__statusbar,
            'liveViewer':self.__liveViewer
            })

        self.__controls.configure()
        self.__toolbox.configure_selected_module()
            

    #Handlers
    def closeEvent(self, e):
        self.__liveViewer.set_visible(False)
        self.__liveViewer.hide()

    def keyPressEvent(self, e):
        self.__toolbox.keyPressEvent(e)
        self.__statusbar.keyPressEvent(e)
        self.__controls.keyPressEvent(e)
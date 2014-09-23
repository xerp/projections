from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui


class AbstractModule(QtGui.QWidget):

    def __init__(self,type_class = None,resource = None):

        type_class = type_class if type_class else QtGui.QWidget
        type_class.__init__(self)

        if resource:
            self._widget = resource
            self._widget.setupUi(self)

        self.instance_variable()
        self.config_components()

    def instance_variable(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def config_components(self):
        pass

from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui


class ProjectionError(Exception):
    pass

class AbstractModule(QtGui.QWidget):

    def __init__(self,parent, type_class = None, resource = None, controls_to_callback={}):

        type_class = type_class if type_class else QtGui.QWidget
        type_class.__init__(self)

        if resource:
            self._widget = resource
            self._widget.setupUi(self)

        self.parent = parent
        self.__controls_to_callback = controls_to_callback

        self.instance_variable()
        self.config_components()

    def instance_variable(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def callback(self,event_name,callback):

        if self.__controls_to_callback:
            button = self.__controls_to_callback[event_name]

            button_name = button.keys()[0]
            button_signal = button.values()[0]

            obj = getattr(self._widget,button_name)

            if not isinstance(button_signal, list):
                QtCore.QObject.connect(obj, QtCore.SIGNAL(button_signal),callback)
            else:
                for button_sig in button_signal:
                    QtCore.QObject.connect(obj, QtCore.SIGNAL(button_sig),callback)

    def set_dependent(self,module_name,module):
        setattr(self,'_{0}'.format(module_name),module)

    def set_dependents(self,modules):
        for module_name, module in modules.iteritems():
            self.set_dependent(module_name,module)

    def config_components(self):
        pass


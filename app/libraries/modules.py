"""Module classes and helpers functions."""

import orm
import configuration as config
import utils

from PyQt4 import QtCore, QtGui
# from jinja2 import Environment, FileSystemLoader
from abc import ABCMeta, abstractmethod


# import app.lib.helpers as helpers


class AbstractModule(QtGui.QWidget):
    """Abstract Module class."""

    __metaclass__ = ABCMeta
    module_enable = True

    def __init__(self, parent, type_class=None, resource=None, callbacks={}):
        """AbstractModule constructor."""
        type_class = type_class if type_class else QtGui.QWidget
        if not issubclass(type_class, QtGui.QDialog):
            super(type_class, self).__init__()
        else:
            super(type_class, self).__init__(parent)

        if resource:
            self._widget = resource
            self._widget.setupUi(self)

        self.__parent = parent
        self.__controls_to_callback = callbacks

        self._instance_variable()
        self._configure()

    def _instance_variable(self):
        """Instanciate module variables."""
        # self.config = helpers.get_app_config()

    def _callback(self, event_name, callback):
        """Register a callback for ui event."""
        if self.__controls_to_callback:
            button = self.__controls_to_callback[event_name]

            button_name = button.keys()[0]
            button_signal = button.values()[0]

            obj = getattr(self._widget, button_name)

            if not isinstance(button_signal, list):
                QtCore.QObject.connect(
                    obj, QtCore.SIGNAL(button_signal), callback)
            else:
                for button_sig in button_signal:
                    QtCore.QObject.connect(
                        obj, QtCore.SIGNAL(button_sig), callback)

    def _disconnect_callback(self, event_name, callback):
        """Unregister a callback."""
        if self.__controls_to_callback:
            button = self.__controls_to_callback[event_name]

            button_name = button.keys()[0]
            button_signal = button.values()[0]

            obj = getattr(self._widget, button_name)

            if not isinstance(button_signal, list):
                QtCore.QObject.disconnect(
                    obj, QtCore.SIGNAL(button_signal), callback)
            else:
                for button_sig in button_signal:
                    QtCore.QObject.disconnect(
                        obj, QtCore.SIGNAL(button_sig), callback)

    @abstractmethod
    def _configure(self):
        """Configure module."""
        pass

    @abstractmethod
    def _get_default_configuration(self):
        """Return default configuration."""
        pass

        # def set_dependent(self, module_name, module):
        #     setattr(self, '_{0}'.format(module_name), module)
        #
        # def set_dependents(self, modules):
        #     for module_name, module in modules.iteritems():
        #         self.set_dependent(module_name, module)


class CoreModule(AbstractModule):
    """CoreModule class."""


class ApplicationModule(AbstractModule):
    """ApplicationModule class."""

    # def _live_config(self):
    #     config = {}
    #
    #     config['text_shadow_color'] = self.config.get(
    #         'LIVE', 'default_text_shadow_color')
    #     config['background_color'] = self.config.get(
    #         'LIVE', 'default_background_color')
    #     config['text_color'] = self.config.get('LIVE', 'default_text_color')
    #
    #     return config

    def _template(self, module):
        """Return template of module."""
        pass
        # path = self.config.get('GENERAL', 'template_path')
        # env = Environment(loader=FileSystemLoader(path))
        # return env.get_template('{0}.html'.format(module)),
        # self._live_config()


class ApplicationDBModule(ApplicationModule):
    """ApplicationDBModule class."""

    def _instance_variable(self):
        super(ApplicationDBModule, self)._instance_variable()
        self._DBAdapter = orm.Adapter(
            config.get_user_database_file(), orm.SQLITE)


class Projection:
    """Projection class."""

    __metaclass__ = ABCMeta
    _projection_item = None

    @abstractmethod
    def process(self, preview_text, **kwargs):
        """Process item."""
        pass

    @_projection_item.setter
    def _projection_item(self, value):
        """Set projection item."""
        self._projection_item = value


class Projectable(Projection):
    """Projectable class."""

    __metaclass__ = ABCMeta

    def __init__(self, projection_method):
        """Projectable constructor."""
        self.projection_method = projection_method


class Slideable(Projection):
    """Slideable class."""

    def get_slide_length(self):
        """Return slides length."""
        try:
            return len(self._projection_item)
        except Exception:
            return 0

    def _projection_item(self, value):
        if isinstance(value, list):
            super(Slideable, self)._projection_item(value)
        else:
            raise utils.ProjectionError("Projection item must be a list")


class ISearchable:
    """Searchable Interface."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self, criteria=None):
        """Search a criteria."""
        pass

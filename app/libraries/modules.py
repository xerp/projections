"""Module classes and helpers functions."""

import orm
import configuration as config
import utils

from PyQt4 import QtCore, QtGui
# from jinja2 import Environment, FileSystemLoader


class AbstractModel:
    """AbstractModel class."""

    def __init__(self, view):
        """AbstractModel Constructor."""
        if isinstance(view, AbstractModule):
            self._view = view
        else:
            raise utils.ProjectionError('view must be AbstractModule')

        self._instance_variable()

    def _instance_variable(self):
        """Instance variables."""
        pass

    def configure_module(self):
        """Configuration of module."""
        pass


class SingletonCoreModule:
    """SingletonCoreModule Decorator."""

    def __init__(self, klass):
        """Constructor."""
        if issubclass(klass, CoreModule):
            self.klass = klass
            self.instance = None
        else:
            raise utils.ProjectionError('klass must be a AbstractModule')

    def __call__(self, parent=None):
        """Call method."""
        if not self.instance:
            self.instance = self.klass(parent)
        return self.instance


class AbstractModule(QtGui.QWidget):
    """Abstract Module class."""

    module_enable = True

    def __init__(self, parent, model_type, type_class=None, resource=None, callbacks={}):
        """AbstractModule constructor."""
        type_class = type_class if type_class else QtGui.QWidget
        if not issubclass(type_class, QtGui.QDialog):
            type_class.__init__(self)
        else:
            type_class.__init__(self, parent)

        if resource:
            self._widget = resource
            self._widget.setupUi(self)

        self.__parent = parent
        self.__controls_to_callback = callbacks

        if model_type and issubclass(model_type, AbstractModel):
            self._model = model_type(self)
        else:
            raise utils.ProjectionError('model must be a AbstractModel')

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

    def _configure(self):
        """Configure module."""
        pass

    def _get_default_configuration(self):
        """Return default configuration."""
        pass


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

    __projection_item = None

    @property
    def _projection_item(self):
        return self._projection_item

    @_projection_item.setter
    def _projection_item(self, value):
        """Set projection item."""
        self.__projection_item = value

    def process(self, preview_text, **kwargs):
        """Process item."""
        pass


class Projectable(Projection):
    """Projectable class."""

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

    def search(self, criteria=None):
        """Search a criteria."""
        pass

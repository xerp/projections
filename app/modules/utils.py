from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui
from jinja2 import Environment, FileSystemLoader

import app.lib.orm as orm


class ProjectionError(Exception):
    pass


class AbstractModule(QtGui.QWidget):
    def __init__(self, parent, type_class=None, resource=None, controls_to_callback={}):

        type_class = type_class if type_class else QtGui.QWidget
        if not issubclass(type_class, QtGui.QDialog):
            type_class.__init__(self)
        else:
            type_class.__init__(self, parent)

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

    def callback(self, event_name, callback):

        if self.__controls_to_callback:
            button = self.__controls_to_callback[event_name]

            button_name = button.keys()[0]
            button_signal = button.values()[0]

            obj = getattr(self._widget, button_name)

            if not isinstance(button_signal, list):
                QtCore.QObject.connect(obj, QtCore.SIGNAL(button_signal), callback)
            else:
                for button_sig in button_signal:
                    QtCore.QObject.connect(obj, QtCore.SIGNAL(button_sig), callback)

    def disconnect_callback(self, event_name, callback):

        if self.__controls_to_callback:
            button = self.__controls_to_callback[event_name]

            button_name = button.keys()[0]
            button_signal = button.values()[0]

            obj = getattr(self._widget, button_name)

            if not isinstance(button_signal, list):
                QtCore.QObject.disconnect(obj, QtCore.SIGNAL(button_signal), callback)
            else:
                for button_sig in button_signal:
                    QtCore.QObject.disconnect(obj, QtCore.SIGNAL(button_sig), callback)

    def set_dependent(self, module_name, module):
        setattr(self, '_{0}'.format(module_name), module)

    def set_dependents(self, modules):
        for module_name, module in modules.iteritems():
            self.set_dependent(module_name, module)


    def config_components(self):
        pass


class ApplicationModule(AbstractModule):
    def _live_config(self):
        config = {}

        config['text_shadow_color'] = self.config.get('LIVE', 'default_text_shadow_color')
        config['background_color'] = self.config.get('LIVE', 'default_background_color')
        config['text_color'] = self.config.get('LIVE', 'default_text_color')

        return config

    def template(self, module):
        path = self.config.get('GENERAL', 'template_path')
        env = Environment(loader=FileSystemLoader(path))
        return env.get_template('{0}.html'.format(module)), self._live_config()

    def configure(self):
        pass


class ApplicationDBModule(ApplicationModule):
    def instance_variable(self):
        super(ApplicationDBModule, self).instance_variable()
        self._DBAdapter = orm.Adapter(self.config.get('GENERAL', 'DB_PATH'), orm.SQLITE)


class ProjectionWizardPage(QtGui.QWizardPage):
    def __init__(self, wizard, title):
        QtGui.QWizardPage.__init__(self, wizard)
        self.setTitle(title)
        self.__layout = QtGui.QVBoxLayout()
        self.setLayout(self.__layout)
        self.callbacks = {}

    def add_widget(self, widget):
        self.__layout.addWidget(widget)

    def callback(self, event, callback):
        self.callbacks[event] = callback

    def validatePage(self):

        if 'validate' in self.callbacks:
            return self.callbacks['validate']()
        else:
            return True


class ProjectionItem:
    __projection_item = None

    def _set_projection_item(self, item):
        self.__projection_item = item

    def get_projection_item(self):
        return self.__projection_item


class Projectable(ProjectionItem):
    def __init__(self, projection_method):
        self.projection_method = projection_method

    def process_projection(self, preview_text, **kwargs):
        pass

    def get_projection_method(self):
        return self.projection_method


class Searchable:
    def search(self, criteria=None):
        pass


class Slideable(ProjectionItem):
    def process_slides(self, preview_text):
        pass

    def get_slide_length(self):
        return len(self.get_projection_item()) if self.get_projection_item() else 0

    def _set_projection_item(self, item):
        if isinstance(item, list):
            ProjectionItem._set_projection_item(self, item)
        else:
            raise ProjectionError("Projection item must be a list")
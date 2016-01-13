"""Toolbox core module."""

from PyQt4 import QtGui
import gui

from app.libraries.modules import CoreModule, SingletonModule
from models import ToolBoxModel


@SingletonModule
class ToolBox(QtGui.QDockWidget, CoreModule):
    """ToolBox core module class."""

    __controls = {
        'color': {'cmdColorScreen': 'clicked()'},
        'live': {'cmdLive': 'toggled(bool)'},
        'fullscreen': {'cmdFullScreen': 'toggled(bool)'},
        'go_to_live': {'cmdGotoLive': 'clicked()'},
        'direct_live': {'cmdDirectToLive': 'toggled(bool)'},
        'image': {'cmdMainView': 'clicked()'},
        'options': {'cbOptions': 'currentIndexChanged(const QString&)'}
    }

    def __init__(self, parent):
        """ToolBox Constructor."""
        super(CoreModule, self).__init__(parent, QtGui.QDockWidget,
                                         gui.Ui_dockProjectionsTools(),
                                         self.__controls)

    def _instance_variable(self):
        self.__model = ToolBoxModel(self)

    def _configure(self):
        self.__model.configure_module()
        self.__model.set_modules()

        self._callback('live', self.set_live)
        self._callback('image', self.__image_view)
        self._callback('color', self.__color_view)
        self._callback('options', self.__option_changed)
        self._callback('direct_live', self.__direct_to_live)
        self._callback('go_to_live', self.go_to_live)

    def __image_view(self):
        self.__model.image_view()

    def __color_view(self):
        self.__model.color_view()

    def __full_screen(self, active):
        self.__model.fullscreen(active)

    def __option_changed(self, text):
        self.configure_selected_module()

    def __direct_to_live(self, active):
        self.__model.direct_to_live(active)

    def go_to_live(self):
        """Go to live."""
        self.__model.go_to_live()

    def reset(self):
        """Reset module."""
        pass

    def configure_selected_module(self):
        """Configure selected module."""
        self.__model.configure_selected_module()

    def selected_option(self):
        """Return selected option."""
        return str(self._widget.cbOptions.currentText())

    def set_live(self, in_live):
        """Set live."""
        self.__model.set_live(in_live)

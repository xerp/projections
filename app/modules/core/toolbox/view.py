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
        super(CoreModule, self).__init__(parent, ToolBoxModel, QtGui.QDockWidget,
                                         gui.Ui_dockProjectionsTools(),
                                         self.__controls)

    def _configure(self):
        self._model.configure_module()
        self._model.set_modules()

        self._callback('live', self.set_live)
        self._callback('image', self.__image_view)
        self._callback('color', self.__color_view)
        self._callback('options', self.__option_changed)
        self._callback('direct_live', self.__direct_to_live)
        self._callback('go_to_live', self.go_to_live)

    def __image_view(self):
        self._model.image_view()

    def __color_view(self):
        self._model.color_view()

    def __full_screen(self, active):
        self._model.fullscreen(active)

    def __option_changed(self, text):
        self.configure_selected_module()

    def __direct_to_live(self, active):
        self._model.direct_to_live(active)

    def go_to_live(self):
        """Go to live."""
        self._model.go_to_live()

    def reset(self):
        """Reset module."""
        pass

    def configure_selected_module(self):
        """Configure selected module."""
        self._model.configure_selected_module()

    def selected_option(self):
        """Return selected option."""
        return str(self._widget.cbOptions.currentText())

    def set_live(self, in_live):
        """Set live."""
        self._model.set_live(in_live)

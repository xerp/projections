"""Statusbar view module."""

import gui

from app.libraries.modules import CoreModule, SingletonModule
from models import StatusBarModel


@SingletonModule
class StatusBar(CoreModule):
    """StatusBar class."""

    def __init__(self, parent):
        """StatusBar Constructor."""
        super(CoreModule, self).__init__(parent, None, gui.Ui_statusBar())

    def _instance_variable(self):
        self.__model = StatusBarModel(self)

    def set_status(self, msg, error=False, time_hide=None, msg_af_hide=''):
        """Set a status."""
        self.__model.set_status(msg, error, time_hide, msg_af_hide)

    def set_live(self, in_live):
        """Set live."""
        self.__model.set_live(in_live)

    def set_button_status(self, text=''):
        """Set button status."""
        self.__model.set_button_status(text)

    def set_full_screen_status(self, active):
        """Set full screen status."""
        self.__model.set_full_screen_status(active)

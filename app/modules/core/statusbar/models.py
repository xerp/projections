"""StatusBar model module."""

import threading
import time

from PyQt4 import QtGui
from app.libraries.modules import AbstractModel


class StatusBarModel(AbstractModel):
    """StatusBarModel class."""

    def set_status(self, msg, error=False, time_hide=None, msg_af_hide=''):
        """Set a status."""
        pixmap = QtGui.QPixmap(
            ":/main/icons/{0}.png".format("error-24" if error else "valid-24"))

        self._view._widget.lblGeneralStatus.setText(msg.capitalize())
        self._view._widget.lblStatusIcon.setVisible(True)
        self._view._widget.lblStatusIcon.setPixmap(pixmap)

        if time_hide:
            def worker():
                time.sleep(time_hide)
                self._view._widget.lblGeneralStatus.setText(msg_af_hide)
                self._view._widget.lblStatusIcon.setVisible(
                    True if msg_af_hide else False)

            thread = threading.Thread(target=worker)
            thread.start()

    def set_live(self, in_live):
        """Set live."""
        self._view.set_button_status()

        self._view._widget.lblLive.setEnabled(in_live)
        self._view._widget.lblLive.setStyleSheet(
            'color: rgb(255, 0, 0);' if in_live else '')

        self._view.set_status('In live' if in_live else 'Off live')

    def set_button_status(self, text=''):
        """Set button status."""
        self._view._widget.lblButton.setText(text)

    def set_full_screen_status(self, active):
        """Set full screen status."""
        self._view._widget.lblFullScreen.setEnabled(active)
        self._view._widget.lblFullScreen.setStyleSheet(
            'color: rgb(0, 0, 255);' if active else '')

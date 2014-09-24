import threading
import time

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.core.statusbar as ui_resource
import app.modules.utils as utils

class StatusBar(utils.AbstractModule):

    def __init__(self,parent):
        utils.AbstractModule.__init__(self,parent,None,ui_resource.Ui_statusBar())

    def set_status(self, msg, error=False, time_to_hide=None, msg_after_hide=''):
        pixmap = QtGui.QPixmap(":/main/icons/{0}.png".format("error-24" if error else "valid-24"))

        self._widget.lblGeneralStatus.setText(msg.capitalize())
        self._widget.lblStatusIcon.setVisible(True)
        self._widget.lblStatusIcon.setPixmap(pixmap)

        if time_to_hide:
            def worker():
                time.sleep(time_to_hide)
                self._widget.lblGeneralStatus.setText(msg_after_hide)
                self._widget.lblStatusIcon.setVisible(True if msg_after_hide else False)

            thread = threading.Thread(target=worker)
            thread.start()

    def set_live(self,in_live):
        self.set_button_status()

        self._widget.lblLive.setEnabled(in_live)
        self._widget.lblLive.setStyleSheet('color: rgb(255, 0, 0);' if in_live else '')

        self.set_status('In live' if in_live else 'Off live')

    def set_button_status(self,text=''):
        self._widget.lblButton.setText(text)

    def set_full_screen_status(self,active):
        self._widget.lblFullScreen.setEnabled(active)
        self._widget.lblFullScreen.setStyleSheet('color: rgb(0, 0, 255);' if active else '')
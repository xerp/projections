from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import re
import app.resources.modules.web_page as ui_resource
import app.modules.utils as utils

from app.lib.helpers import get_projections_font, set_alignment
from sqlalchemy import Column, Integer, String, Text, ForeignKey,func
from sqlalchemy.orm import relationship
from ConfigParser import ConfigParser

def configure_options(**kwargs):
    options = WebPageOptions(kwargs['controls'].module_options_panel)
    options.set_dependents(kwargs)
    options.configure()

    return options


class WebPageOptions(utils.ApplicationModule):

    __controls = {
        'clear_text':{'cmdClearText':'clicked()'},
    }

    def __init__(self,parent):
        utils.ApplicationModule.__init__(self,parent,None,ui_resource.Ui_Form(),self.__controls)

    def config_components(self):

        self.callback('clear_text',self.__clear_text)

    def configure(self):

        self._controls.search_in_history = True
        self._controls.add_module_options(self)
        self._controls.set_enable_slides(False)
        self._controls.set_enable_live_font_size(False)

        self._toolbox.set_go_to_live_callback(self.__go_to_live)
        self._statusbar.set_status('Web page module loaded successfully')

    def __clear_text(self):
        self._widget.txtWebPage.clear()

    def __view_page(self):

        if self._toolbox.direct_live:
            self._toolbox.go_to_live()

    def __go_to_live(self,previewText):
        url = str(self._widget.txtWebPage.toPlainText())

        if url:
            if 'http://' not in url and 'https://' not in url:
                url = 'http://{0}'.format(url)
                
            self._controls.add_to_history(url)
            return {'method':'url','url':url}

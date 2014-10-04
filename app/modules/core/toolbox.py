from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import pkgutil
import importlib
import app.resources.modules.core.toolbox as ui_resource
import app.modules.utils as utils

MODULES_TO_EXCLUDE = ['utils',]

class ToolBox(QtGui.QDockWidget,utils.AbstractModule):

    __controls = {
        'color': {'cmdColorScreen':'clicked()'},
        'live':{'cmdLive':'toggled(bool)'},
        'fullscreen':{'cmdFullScreen':'toggled(bool)'},
        'go_to_live':{'cmdGotoLive':'clicked()'},
        'direct_live':{'cmdDirectToLive':'toggled(bool)'},
        'image':{'cmdMainView':'clicked()'},
        'options' : {'cbOptions': 'currentIndexChanged(const QString&)'} 
    }

    def __init__(self,parent):
        utils.AbstractModule.__init__(self,
            parent,QtGui.QDockWidget,ui_resource.Ui_dockProjectionsTools(),self.__controls)

    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

        self.in_live = False
        self.direct_live = False

    def config_components(self):
        self._widget.cmdColorScreen.setText('{0} (F9)'.format(self.config.get('LIVE', 'DEFAULT_COLOR').upper()))
        self._widget.cmdColorScreen.setShortcut('F9')

        self.__set_modules()

        self.callback('live',self.set_live)
        self.callback('image',self.__image_view)
        self.callback('color',self.__color_view)
        self.callback('fullscreen',self.__full_screen)
        self.callback('options',self.__option_changed)
        self.callback('direct_live',self.__direct_to_live)
        self.callback('go_to_live',self.go_to_live)


    def __set_modules(self):

        modules = filter(lambda mod: 'app.modules.' in mod and 'core' not in mod,
            map(lambda (m,n,i): n ,pkgutil.walk_packages('app.modules')))
        modules = map(lambda mod: mod.split('.')[-1].capitalize(),modules)
        modules = filter(lambda mod: mod.lower() not in MODULES_TO_EXCLUDE,modules)

        self._widget.cbOptions.addItems(modules)


    def __image_view(self):
        
        try:
            self._liveViewer.set_image(self._controls.selected_image())

            self._statusbar.set_button_status('Image View')
            self._statusbar.set_status('Live in Image View')
        
        except utils.ProjectionError, e:
            self._statusbar.set_status(e.message, True,5)

    def __color_view(self):
        self._liveViewer.set_color()

        color = self.config.get('LIVE', 'DEFAULT_COLOR').upper()
        self._statusbar.set_button_status(color)
        self._statusbar.set_status('Live in {0}'.format(color))


    def __full_screen(self, active):
        self._liveViewer.set_full_screen(active)
        self._statusbar.set_full_screen_status(active)

    def __option_changed(self,text):
        self.configure_selected_module()

    def __direct_to_live(self, active):
        self.direct_live = active
        self._statusbar.set_status('Direct live {0}'.format('on' if active else 'off'))

    def go_to_live(self):

        text = self._previewer.toPlainText()

        if text:
            try:
                returnedText,encode = self.go_to_live_callback(text)
                self._liveViewer.set_text(returnedText,self._controls.live_font(),encode)    
            except AttributeError:
                self._liveViewer.set_text(self._controls.slides[self._controls.slide_position],self._controls.live_font())
                self._controls.seeker()

        self._statusbar.set_status('View refreshed')

    def set_go_to_live_callback(self,callback):
        setattr(self,'go_to_live_callback',callback)

    def reset(self):
        try:
            del(self.go_to_live_callback)
        except Exception:
            pass

    def configure_selected_module(self):

        module = self._widget.cbOptions.currentText()
        module = importlib.import_module('app.modules.{0}'.format(str(module).lower()))

        # try:
        self._controls.reset()
        self._previewer.reset()
        self.reset()
        module.configure_options(
            controls=self._controls,
            statusbar=self._statusbar, 
            previewer=self._previewer, 
            liveViewer=self._liveViewer, 
            toolbox=self)
        self._statusbar.set_status('TODO:configure_selected_module')
        # except AttributeError, e:
        #     self._controls.hide_module_options()
        #     self._controls.hide_search_box()
        #     self._statusbar.set_status('{0} module dont have options'.format(module.__name__.split('.')[-1]),time_to_hide=5)


    def set_live(self,in_live):

        self.in_live = in_live

        self._widget.cmdFullScreen.setChecked(False)
        self._widget.cmdDirectToLive.setChecked(False)

        self._widget.cmdDirectToLive.setEnabled(in_live)
        self._widget.cmdGotoLive.setEnabled(in_live)
        self._widget.cmdMainView.setEnabled(in_live)
        self._widget.cmdColorScreen.setEnabled(in_live)
        self._widget.cmdFullScreen.setEnabled(in_live)

        self._widget.cmdLive.setChecked(in_live)

        self._statusbar.set_live(in_live)
        self._controls.set_live(in_live)

        self._liveViewer.set_visible(self.in_live, self._controls.selected_screen())
        self._liveViewer.set_color(Qt.red)
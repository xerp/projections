from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.modules
import app.resources.modules.core.toolbox as ui_resource
import app.modules.utils as utils

MODULES_TO_EXCLUDE = ['core','utils','songs']

class ToolBox(QtGui.QDockWidget,utils.AbstractModule):

    __controls = {
        'color': {'cmdColorScreen':'clicked()'},
        'live':{'cmdLive':'toggled(bool)'},
        'fullscreen':{'cmdFullScreen':'toggled(bool)'},
        'go_live':{'cmdGotoLive':'clicked()'},
        'direct_live':{'cmdDirectToLive':'toggled(bool)'},
        'image':{'cmdMainView':'clicked()'} 
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

    def __set_modules(self):

        modules = app.modules.__dict__
        modules = filter(lambda m: '__' not in m and m not in MODULES_TO_EXCLUDE,modules)
        modules.insert(0,'bible')

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


    def configure_selected_module(self):

        module = __import__('app.modules.bible').modules.bible
        module.configure_options(self._controls)


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

        # self.__window.txtPreview.setFont(get_projections_font(dict(conf.items('FONT_PREVIEW'))))
        # self.__window.txtSearch.setPlaceholderText("Search in bible (F3)")


    #     def rbBible_clicked(self):
#         self.__window.txtSearch.setPlaceholderText('Search in bible (F3)')
#         self.__window.txtSearch.setCompleter(None)

#         self.__window.txtSearch.selectAll()
#         self.__window.txtSearch.setFocus()

#         self.__window.cmdEditSong.setEnabled(False)
#         self.__window.cmdDeleteSong.setEnabled(False)
#         self.selected_song = None

#         self.set_status('Bible search')

    #     def cmdDirectToLive_toggled(self, active):
#         self.direct_live = active
#         self.set_status('Direct live {0}'.format('on' if active else 'off'))

#     def cmdGotoLive_clicked(self):
#         text = self.__window.txtPreview.toPlainText()

#         if text:
#             self.full_screen.set_text(self.slides[self.slide_position],
#                                       self.__window.sLiveFont.value())

#             if self.in_live:
#                 self.set_seeker()

#         self.set_status('View refreshed')


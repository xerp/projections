from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.core.controls as ui_resource
import app.modules.utils as utils

from app.lib.helpers import get_images_view, ImagesViewModel,get_screens

class Controls(QtGui.QDockWidget,utils.AbstractModule):

    __controls = {
        'live_font': {'sLiveFont':['sliderMoved(int)','valueChanged(int)']},
        'refresh_images':{'cmdRefreshImageView':'clicked()'},
        'refresh_screens':{'cmdRefreshLiveScreens':'clicked()'}
    }

    def __init__(self,parent):
        utils.AbstractModule.__init__(self,
            parent,QtGui.QDockWidget,ui_resource.Ui_projectionsControls(),self.__controls)

        self.__set_live_screens()

    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

        self.slides = []
        self.slide_length = len(self.slides)
        self.slide_position = 0

        self.module_options_panel = self._widget.saModuleOptions

    def config_components(self):
        self.module_options_panel.setVisible(False)
        self._widget.txtSearch.setVisible(False)

        self.callback('refresh_images',self.__set_images)
        self.callback('refresh_screens',self.__set_live_screens)
        self.callback('live_font',self.__live_font)


    def __set_live_screens(self):
        screens = get_screens()

        self._widget.cbLiveScreens.model().clear()
        self._widget.cbLiveScreens.addItems(map(lambda s: 'Screen {0}'.format(s), range(1, screens + 1)))

        if screens >= self.config.getint('LIVE', 'DEFAULT_SCREEN'):
            self._widget.cbLiveScreens.setCurrentIndex(self.config.getint('LIVE', 'DEFAULT_SCREEN') - 1)

    def __seeker(self):
        self.__remove_buttons_slides()

        if self.in_live and self.slide_length > 1:
            self.__set_buttons_slides(self.slide_length)

            self._widget.cmdPrevious.setEnabled(False)
            self._widget.cmdNext.setEnabled(True)

    def __remove_buttons_slides(self):

        for index in range(0, self._widget.cmdSlides.count() + 1):
            row, col, rspan, cspan = self._widget.cmdSlides.getItemPosition(index)
            item = self._widget.cmdSlides.itemAtPosition(row, col)

            if item:
                item.widget().deleteLater()

    def __set_buttons_slides(self, max_slides):
        self.__remove_buttons_slides()

        cols = 5
        for slide in range(1, max_slides + 1):
            button = QtGui.QPushButton(str(slide))

            button.setMaximumSize(QtCore.QSize(30, 30))
            button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

            #FIXME button.clicked.connect(partial(self.onBtnSlide_clicked, slide))

            items = self._widget.cmdSlides.count()
            row = items / cols
            col = items % cols

            self._widget.cmdSlides.addWidget(button, row, col)

    def __set_images(self):
        try:
            images = get_images_view()
            model = ImagesViewModel(images, self._widget.cbImagesView)
            self._widget.cbImagesView.setModel(model)

            try:
                self._widget.cbImagesView.setCurrentIndex(images.index(self.config.get('GENERAL', 'DEFAULT_IMAGE')))
            except Exception:
                pass

        except Exception, e:
            raise e

    def __live_font(self,value):

        if self._toolbox.in_live:
            try:
                pass #self.__liveViewer.set_text(self.slides[self.slide_position], value)
            except IndexError:
                pass

        self._statusbar.set_status('Font size: {0} point(s)'.format(value), time_to_hide=2)

    def configure_search_box(self):
        self._widget.txtSearch.setVisible(True)

        self._widget.txtSearch.selectAll()
        self._widget.txtSearch.setFocus()


    def add_module_options(self,widget):
        vBoxMainLayout = QtGui.QVBoxLayout()

        vBoxMainLayout.addWidget(widget)

        self.module_options_panel.setLayout(vBoxMainLayout)
        self.module_options_panel.setVisible(True)

    def configure(self):

        try:

            self.__set_images()

            self._widget.sLiveFont.setValue(
             int(dict(self.config.items('FONT_LIVE')).get('size', self.config.getint('LIVE', 'DEFAULT_FONT_SIZE'))))

        except Exception, e:
            self._statusbar.set_status(e.message,True,5)

    def set_live(self,in_live):
        self._widget.cbLiveScreens.setEnabled(not in_live)

        if not in_live:
            self._widget.cmdPrevious.setEnabled(False)
            self._widget.cmdNext.setEnabled(False)

        self.__seeker

    def selected_screen(self):
        return self._widget.cbLiveScreens.currentIndex() + 1

    def selected_image(self):
        return self._widget.cbImagesView.model().selected()

    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_F3:
            self._widget.txtSearch.selectAll()
            self._widget.txtSearch.setFocus()



    #     def set_slides(self, whole_text, delimiter, limit=conf.getint('BIBLE', 'FORWARD_LIMIT')):

#         if self.__window.chkSearchForward.isChecked():
#             splitted = whole_text.split(delimiter)[:limit]
#         else:
#             splitted = whole_text.split(delimiter)

#         self.slides = filter(lambda s: s and s != '(END)', splitted)
#         self.slide_length = len(self.slides)
#         self.slide_position = 0

#         self.set_seeker()

    #     def txtSearch_enter_pressed(self):
#         text = self.__window.txtSearch.text()
#         result = ''
#         delimiter = ''

#         self.set_status('Ready')

#         if self.__window.rbBible.isChecked():
#             if self.__window.chkSearchForward.isChecked():
#                 text = '{0}-'.format(text)

#             delimiter = bible.DELIMITER
#             try:
#                 result = bible.search_verse(text)
#             except bible.BibleError, e:
#                 self.set_status(str(e), True)

#         else:
#             delimiter = songs.DELIMITER

#             try:
#                 self.selected_song = self.__window.txtSearch.completer().model().selected()
#                 result = self.selected_song.body

#                 self.__window.cmdEditSong.setEnabled(True)
#                 self.__window.cmdDeleteSong.setEnabled(True)
#             except songs.SongError, e:
#                 self.set_status(str(e), True)

#         self.set_slides(result, delimiter)

#         self.__window.txtPreview.setText(result)

#         if self.direct_live:
#             self.full_screen.set_text(self.slides[self.slide_position],
#                                       self.__window.sLiveFont.value())


#     def cmdPrevious_clicked(self):

#         self.slide_position -= 1
#         self.full_screen.set_text(self.slides[self.slide_position],
#                                   self.__window.sLiveFont.value())

#         self.__window.cmdNext.setEnabled(True)
#         self.__window.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

#     def cmdNext_clicked(self):

#         self.slide_position += 1
#         self.full_screen.set_text(self.slides[self.slide_position],
#                                   self.__window.sLiveFont.value())

#         self.__window.cmdPrevious.setEnabled(True)
#         self.__window.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)

#     def onBtnSlide_clicked(self, button_num):

#         self.slide_position = button_num - 1
#         self.full_screen.set_text(self.slides[self.slide_position],
#                                   self.__window.sLiveFont.value())

#         self.__window.sLiveFont.setValue(
#             int(dict(conf.items('FONT_LIVE')).get('size', conf.get('LIVE', 'DEFAULT_FONT_SIZE'))))

#         self.__window.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)
#         self.__window.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import os
import app.resources.modules.core.controls as ui_resource
import app.modules.utils as utils
from functools import partial

from app.lib.helpers import get_images_view, ImagesViewModel,get_screens

class Controls(QtGui.QDockWidget,utils.AbstractModule):

    __controls = {
        'live_font': {'sLiveFont':['sliderMoved(int)','valueChanged(int)']},
        'refresh_images':{'cmdRefreshImageView':'clicked()'},
        'previous_slide':{'cmdPrevious':'clicked()'},
        'next_slide':{'cmdNext':'clicked()'},
        'refresh_screens':{'cmdRefreshLiveScreens':'clicked()'},
        'search':{'txtSearch':'returnPressed()'}
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

        self.search_in_history = False
        self.__historyPosition = 0
        self.__history = []

        self.module_options_panel = self._widget.saModuleOptions

    def config_components(self):
        self.module_options_panel.setVisible(False)
        self._widget.txtSearch.setVisible(False)

        self._widget.sLiveFont.setValue(self.config.getint('LIVE', 'DEFAULT_FONT_SIZE'))

        self.callback('refresh_images',self.__set_images)
        self.callback('refresh_screens',self.__set_live_screens)
        self.callback('live_font',self.__live_font)
        self.callback('previous_slide',self.__previous_slide)
        self.callback('next_slide',self.__next_slide)


    def __set_live_screens(self):
        screens = get_screens()

        self._widget.cbLiveScreens.model().clear()
        self._widget.cbLiveScreens.addItems(map(lambda s: 'Screen {0}'.format(s), range(1, screens + 1)))

        if screens >= self.config.getint('LIVE', 'DEFAULT_SCREEN'):
            self._widget.cbLiveScreens.setCurrentIndex(self.config.getint('LIVE', 'DEFAULT_SCREEN') - 1)

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

            button.clicked.connect(partial(self.__slide_click, slide))

            items = self._widget.cmdSlides.count()
            row = items / cols
            col = items % cols

            self._widget.cmdSlides.addWidget(button, row, col)

    def __set_images(self):

        try:
            self._widget.cbImagesView.setInsertPolicy(6)
            images = get_images_view()
            for img in images:
                self._widget.cbImagesView.addItem(QtGui.QIcon(img),img.split(os.sep)[-1].split('.')[0])

            self._widget.cbImagesView.setIconSize(QtCore.QSize(50,50))

            try:
                self._widget.cbImagesView.setCurrentIndex(images.index(self.config.get('GENERAL', 'DEFAULT_IMAGE')))
            except Exception:
                pass

        except Exception, e:
            print e


    def __live_font(self,value):

        if self._toolbox.in_live:
            try:
                self._liveViewer.set_font_size(value)
            except IndexError:
                pass

        self._statusbar.set_status('Font size: {0} point(s)'.format(value), time_to_hide=2)

    def __previous_slide(self):

        self.slide_position -= 1
        self._liveViewer.set_text(self.slides[self.slide_position],self._widget.sLiveFont.value())

        self._widget.cmdNext.setEnabled(True)
        self._widget.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

    def __next_slide(self):

        self.slide_position += 1
        self._liveViewer.set_text(self.slides[self.slide_position],self._widget.sLiveFont.value())

        self._widget.cmdPrevious.setEnabled(True)
        self._widget.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)

    def __slide_click(self, button_num):

        self.slide_position = button_num - 1
        self._liveViewer.set_text(self.slides[self.slide_position],self._widget.sLiveFont.value())

        self._widget.sLiveFont.setValue(self.config.getint('LIVE', 'DEFAULT_FONT_SIZE'))

        self._widget.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)
        self._widget.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

    def configure_search_box(self,callback = None):
        self._widget.txtSearch.setVisible(True)

        self._widget.txtSearch.selectAll()
        self._widget.txtSearch.setFocus()

        if callback:
            self.callback('search',callback)

    def search_box_text(self):
        return self._widget.txtSearch.text()

    def set_search_box_text(self,text = None):

        if text:
            self._widget.txtSearch.setText(text)

    def clear_search_box(self):
        self._widget.txtSearch.setText('')

    def live_font(self):
        return self._widget.sLiveFont.value()

    def set_slide_callback(self,callback):
        setattr(self,'slide_callback',callback)

    def add_module_options(self,widget):

        self.module_options_panel.setWidget(widget)
        self.module_options_panel.setVisible(True)

    def hide_module_options(self):
        self.module_options_panel.setVisible(False)

    def hide_search_box(self):
        self._widget.txtSearch.setVisible(False)

    def reset(self):
        self.set_enable_slides(True)
        self._widget.txtSearch.setVisible(False)
        self.clear_search_box()

        self.search_in_history = False
        self.__historyPosition = 0
        self.__history = []

        try:
            del(self.slide_callback)
        except Exception:
            pass 

    def configure(self):

        try:

            self.__set_images()

        except Exception, e:
            self._statusbar.set_status(e.message,True,5)

    def seeker(self):
        self.__remove_buttons_slides()

        self._widget.cmdPrevious.setEnabled(False)
        self._widget.cmdNext.setEnabled(False)
        
        if self._toolbox.in_live and self.slide_length > 1:
            self.__set_buttons_slides(self.slide_length)

            self._widget.cmdPrevious.setEnabled(False)
            self._widget.cmdNext.setEnabled(True)

    def selected_screen(self):
        return self._widget.cbLiveScreens.currentIndex() + 1

    def selected_image(self):
        return self._widget.cbImagesView.model().selected()

    def set_enable_slides(self,enable):
        self._widget.cmdNext.setVisible(enable)
        self._widget.cmdPrevious.setVisible(enable)
        self._widget.saCmdSlides.setVisible(enable)

    def set_slides(self, whole_text,**kwarg):

        if hasattr(self,'slide_callback'):
            self.slides = self.slide_callback(whole_text,**kwarg)
        else:
            if 'delimiter' in kwarg and 'limit' in kwarg:
                splitted = whole_text.split(kwarg['delimiter'])[:kwarg['limit']]
            elif 'delimiter' in kwarg:
                splitted = whole_text.split(kwarg['delimiter'])
            else:
                splitted = whole_text

            self.slides = filter(lambda s: s, splitted)

        self.slide_length = len(self.slides)
        self.slide_position = 0

        self.seeker()

    def add_to_history(self,text):
        if text and text not in self.__history:
            self.__history.append(text)
            self.__historyPosition = len(self.__history)

    def set_live(self,in_live):
        self._widget.cbLiveScreens.setEnabled(not in_live)

        if not in_live:
            self._widget.cmdPrevious.setEnabled(False)
            self._widget.cmdNext.setEnabled(False)

        self.seeker()

    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_F3:
            self._widget.txtSearch.selectAll()
            self._widget.txtSearch.setFocus()

        if e.key() == Qt.Key_Plus:
            self._widget.sLiveFont.setValue(self.live_font() + 3)

        if e.key() == Qt.Key_Minus:
            self._widget.sLiveFont.setValue(self.live_font() - 3)

        if self.search_in_history:
            if e.key() == Qt.Key_PageDown:
                self.__historyPosition += 1
                try:
                    self.set_search_box_text(self.__history[self.__historyPosition])
                except IndexError:
                    self.__historyPosition = len(self.__history) - 1
                    self.clear_search_box()

            if e.key() == Qt.Key_PageUp:
                if self.__history and self.__historyPosition >= 0:
                    self.__historyPosition -= 1
                    self.set_search_box_text(self.__history[self.__historyPosition])
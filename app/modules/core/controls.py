import os
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.core.controls as ui_resource
import app.modules.utils as utils
from app.lib.helpers import get_images_view, get_screens, open_directory, is_valid_directory


class Controls(QtGui.QDockWidget, utils.AbstractModule):
    __controls = {
        'live_font': {'sLiveFont': ['sliderMoved(int)', 'valueChanged(int)']},
        'refresh_images': {'cmdRefreshImageView': 'clicked()'},
        'open_image_dir': {'cmdOpenImageDirectory': 'clicked()'},
        'previous_slide': {'cmdPrevious': 'clicked()'},
        'next_slide': {'cmdNext': 'clicked()'},
        'refresh_screens': {'cmdRefreshLiveScreens': 'clicked()'},
        'search': {'txtSearch': 'returnPressed()'},
        'previous_history': {'cmdPreviousHistory': 'clicked()'},
        'next_history': {'cmdNextHistory': 'clicked()'}
    }

    def __init__(self, parent):
        utils.AbstractModule.__init__(self,
                                      parent, QtGui.QDockWidget, ui_resource.Ui_projectionsControls(), self.__controls)

        self.__set_live_screens()

    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

        self.slide_position = 0

        self.__search_in_history = False
        self.__history = {}

        self.module_options_panel = self._widget.saModuleOptions

    def config_components(self):
        self.module_options_panel.setVisible(False)
        self._widget.txtSearch.setVisible(False)

        self._widget.sLiveFont.setValue(self.config.getint('LIVE', 'DEFAULT_FONT_SIZE'))

        self.callback('refresh_images', self.__set_images)
        self.callback('open_image_dir', self.__open_image_dir)
        self.callback('refresh_screens', self.__set_live_screens)
        self.callback('live_font', self.__live_font)
        self.callback('previous_slide', self.__previous_slide)
        self.callback('next_slide', self.__next_slide)
        self.callback('previous_history', self.__previous_history)
        self.callback('next_history', self.__next_history)


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
                del (item)

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
            images = get_images_view(self.config.get('GENERAL', 'IMAGES_DIRS'))
            setattr(self._widget.cbImagesView, 'images', images)

            self._widget.cbImagesView.model().clear()
            for img in images:
                self._widget.cbImagesView.addItem(QtGui.QIcon(img), img.split(os.sep)[-1].split('.')[0])

            self._widget.cbImagesView.setIconSize(QtCore.QSize(50, 50))

            try:
                self._widget.cbImagesView.setCurrentIndex(images.index(self.config.get('GENERAL', 'DEFAULT_IMAGE')))
            except Exception:
                pass

        except Exception, e:
            print e

    def __open_image_dir(self):

        if self.config.get('GENERAL', 'IMAGES_DIRS'):
            if is_valid_directory(self.config.get('GENERAL', 'IMAGES_DIRS')):
                open_directory(self.config.get('GENERAL', 'IMAGES_DIRS'))
            else:
                self._statusbar.set_status("Image directory doesn't exist", True, time_to_hide=2)
        else:
            self._statusbar.set_status("Image directory property isn't set", True, time_to_hide=2)

    def __live_font(self, value):
        self._statusbar.set_status('Font size: {0} point(s)'.format(value), time_to_hide=2)

    def __previous_slide(self):

        if self._toolbox.selected_module and isinstance(self._toolbox.selected_module, utils.Slideable):
            module = self._toolbox.selected_module

            self.slide_position -= 1
            kwarg = {'item': module.get_projection_item()[self.slide_position],
                     'font_size': self._widget.sLiveFont.value()}
            self._liveViewer.set_text(**kwarg)

            self._widget.cmdNext.setEnabled(True)
            self._widget.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

    def __next_slide(self):

        if self._toolbox.selected_module and isinstance(self._toolbox.selected_module, utils.Slideable):
            module = self._toolbox.selected_module

            self.slide_position += 1
            kwarg = {'item': module.get_projection_item()[self.slide_position],
                     'font_size': self._widget.sLiveFont.value()}
            self._liveViewer.set_text(**kwarg)

            self._widget.cmdPrevious.setEnabled(True)
            self._widget.cmdNext.setEnabled(False if self.slide_position == (module.get_slide_length() - 1) else True)

    def __slide_click(self, button_num):
        if self._toolbox.selected_module and isinstance(self._toolbox.selected_module, utils.Slideable):
            module = self._toolbox.selected_module

            self.slide_position = button_num - 1
            kwarg = {'item': module.get_projection_item()[self.slide_position],
                     'font_size': self._widget.sLiveFont.value()}
            self._liveViewer.set_text(**kwarg)

            self._widget.cmdNext.setEnabled(False if self.slide_position == (module.get_slide_length() - 1) else True)
            self._widget.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

    def __history_control_text(self, text):

        if hasattr(self, 'history_control_method'):
            self.history_control_method(text)
        else:
            self.set_search_box_text(text)


    def __clear_history_control(self):

        if hasattr(self, 'history_control_method'):
            self.history_control_method('')
        else:
            self._widget.txtSearch.setText('')

    def __next_history(self):

        option = self._toolbox.selected_option()

        if option in self.__history:
            self.__history[option]['position'] += 1
            try:
                position = self.__history[option]['position']
                self.__history_control_text(self.__history[option]['data'][position])
            except IndexError:
                self.__history[option]['position'] = len(self.__history[option]['data'])
                self.__clear_history_control()

    def __previous_history(self):

        option = self._toolbox.selected_option()

        if option in self.__history:
            if self.__history[option]['position'] > 0:
                self.__history[option]['position'] -= 1
                try:
                    position = self.__history[option]['position']
                    self.__history_control_text(self.__history[option]['data'][position])
                except IndexError:
                    self.__history[option]['position'] += 1
            else:
                self.__history[option]['position'] = 0
                position = self.__history[option]['position']
                self.__history_control_text(self.__history[option]['data'][position])


    def search_in_history(self, option):

        self.__search_in_history = option

        self._widget.cmdPreviousHistory.setVisible(option)
        self._widget.cmdNextHistory.setVisible(option)

    def configure_search_box(self, module):
        self._widget.txtSearch.setVisible(True)

        self._widget.txtSearch.selectAll()
        self._widget.txtSearch.setFocus()

        if module and isinstance(module, utils.Searchable):
            self.callback('search', module.search)


    def search_box_text(self):
        return self._widget.txtSearch.text()

    def set_search_box_text(self, text=None):
        if text:
            self._widget.txtSearch.setText(text)

    def clear_search_box(self):
        self._widget.txtSearch.setText('')

    def live_font(self):
        return self._widget.sLiveFont.value()

    def add_module_options(self, widget):
        self.module_options_panel.setWidget(widget)
        self.module_options_panel.setVisible(True)


    def hide_module_options(self):
        self.module_options_panel.setVisible(False)


    def hide_search_box(self):
        self._widget.txtSearch.setVisible(False)


    def reset(self):
        self.set_enable_slides(True)
        self.set_enable_live_font_size(True)
        self._widget.txtSearch.setVisible(False)
        self.clear_search_box()

        self.search_in_history(False)

        try:
            del (self.history_control_method)
        except Exception, e:
            pass

    def configure(self):
        try:
            self.__set_images()
        except Exception, e:
            self._statusbar.set_status(e.message, True, 5)


    def seeker(self):
        self.__remove_buttons_slides()

        self._widget.cmdPrevious.setEnabled(False)
        self._widget.cmdNext.setEnabled(False)

        if self._toolbox.in_live and self._toolbox.selected_module.get_slide_length() > 1:
            self.__set_buttons_slides(self._toolbox.selected_module.get_slide_length())

            self._widget.cmdPrevious.setEnabled(False)
            self._widget.cmdNext.setEnabled(True)


    def selected_screen(self):
        return self._widget.cbLiveScreens.currentIndex() + 1


    def selected_image(self):
        image_name = str(self._widget.cbImagesView.currentText())
        if image_name:
            return \
                filter(lambda img: img.split(os.sep)[-1].split('.')[0] == image_name, self._widget.cbImagesView.images)[
                    0]


    def set_enable_slides(self, enable):
        self._widget.cmdNext.setVisible(enable)
        self._widget.cmdPrevious.setVisible(enable)
        self._widget.saCmdSlides.setVisible(enable)


    def set_enable_live_font_size(self, enable):
        self._widget.sLiveFont.setVisible(enable)
        self._widget.lblLiveFont.setVisible(enable)


    def set_slides(self):
        self.slide_position = 0
        self.seeker()


    def add_to_history(self, text):
        option = self._toolbox.selected_option()

        if option not in self.__history:
            self.__history[option] = {'position': 0, 'data': []}

        if text and text not in self.__history[option]['data']:
            self.__history[option]['data'].append(text)
            self.__history[option]['position'] = len(self.__history[option]['data'])


    def set_history_control(self, control_method):
        setattr(self, 'history_control_method', control_method)

        self.search_in_history(True)


    def set_live(self, in_live):
        self._widget.cbLiveScreens.setEnabled(not in_live)

        if not in_live:
            self._widget.cmdPrevious.setEnabled(False)
            self._widget.cmdNext.setEnabled(False)

        if self._toolbox.selected_module and isinstance(self._toolbox.selected_module,utils.Slideable):
            self.seeker()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F3:
            self._widget.txtSearch.selectAll()
            self._widget.txtSearch.setFocus()

        if e.key() == Qt.Key_Plus:
            self._widget.sLiveFont.setValue(self.live_font() + 3)

        if e.key() == Qt.Key_Minus:
            self._widget.sLiveFont.setValue(self.live_font() - 3)

        if self.__search_in_history:
            if e.key() == Qt.Key_PageDown:
                self.__next_history()

            if e.key() == Qt.Key_PageUp:
                self.__previous_history()

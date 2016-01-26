"""Controls view module."""

import gui

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from app.libraries.modules import CoreModule
from models import ControlsModel, HistoryModel, SliderModel

from app.modules.core import core_modules


class Controls(QtGui.QDockWidget, CoreModule):
    """Controls class."""

    __controls = {
        'live_font': {'sLiveFont': ['sliderMoved(int)', 'valueChanged(int)']},
        'refresh_images': {'cmdRefreshImageView': 'clicked()'},
        'open_images_directory': {'cmdOpenImageDirectory': 'clicked()'},
        'previous_slide': {'cmdPrevious': 'clicked()'},
        'next_slide': {'cmdNext': 'clicked()'},
        'refresh_screens': {'cmdRefreshLiveScreens': 'clicked()'},
        'search': {'txtSearch': 'returnPressed()'},
        'previous_history': {'cmdPreviousHistory': 'clicked()'},
        'next_history': {'cmdNextHistory': 'clicked()'}
    }

    __setters__ = {}

    def __init__(self, parent):
        """Controls Constructor."""
        super(CoreModule, self).__init__(parent, ControlsModel, QtGui.QDockWidget,
                                         gui.Ui_projectionsControls(),
                                         self.__controls)

    def __setattr__(self, name, value):
        """Set attributes."""
        if self.__setters__:
            prop = self.__setters__[name]
            return prop(value)
        else:
            super(CoreModule, self).__setattr__(name, value)

    def _instance_variable(self):
        self._history_model = HistoryModel(self)
        self._slider_model = SliderModel(self)

    def _configure(self):
        self._model.configure_module()
        self._history_model.configure_module()

        self._callback('refresh_images', self.__set_images)
        self._callback('open_images_directory', self.__open_images_directory)
        self._callback('refresh_screens', self.__set_live_screens)
        self._callback('live_font', self.__live_font)
        self._callback('previous_slide', self.__previous_slide_clicked)
        self._callback('next_slide', self.__next_slide_clicked)
        self._callback('previous_history', self.__previous_history_clicked)
        self._callback('next_history', self.__next_history_clicked)

        self.__dict__['search_box_text'] = self._widget.txtSearch.text()
        self.__dict__['live_font'] = self._widget.sLiveFont.value()
        self.__dict__['selected_screen'] = self.__selected_screen()

        self.__dict__['selected_image'] = self._model.selected_image
        # self.__dict__['live'] = self._model.live
        self.__dict__['slide_position'] = self._slider_model.slide_position
        # self.__dict__['history_control'] = self._history_model.history_control
        # self.__dict__[
        #     'search_in_history'] = self._history_model.search_in_history

        self.__setters__['search_text'] = self._widget.txtSearch.setText
        self.__setters__['enable_live_font'] = self.__set_enable_live_font

    def __set_live_screens(self):
        self._model.set_live_screen()

    def __set_images(self):
        self._model.set_images()

    def __open_images_directory(self):
        self._model.open_images_directory()

    def __live_font(self, value):
        core_modules.get_status_bar().set_status(
            'Font size: {0} point(s)'.format(value), time_hide=2)

    def __previous_slide_clicked(self):
        self._slider_model.previous_slide_clicked()

    def __next_slide_clicked(self):
        self._slider_model.next_slide_clicked()

    def __next_history_clicked(self):
        self._history_model.next_history_clicked()

    def __previous_history_clicked(self):
        self._history_model.previous_history_clicked()

    def __selected_screen(self):
        return self._widget.cbLiveScreens.currentIndex() + 1

    def __set_enable_live_font(self, enable):
        self._widget.sLiveFont.setVisible(enable)
        self._widget.lblLiveFont.setVisible(enable)

    # FIXME
    # def slider_seeker(self):
    #     self._slider_model.slider_seeker()

    # FIXME
    # def set_enable_slides(self, enable):
    #     self._slider_model.set_enable_slides(enable)

    def configure_search_box(self, module):
        """Configure search box."""
        self._model.configure_search_box(module)

    def add_module_options(self, widget):
        """Add module options."""
        self._module_options_panel.setWidget(widget)
        self._module_options_panel.setVisible(True)

    def hide_module_options(self):
        """Hide module options."""
        self._module_options_panel.setVisible(False)

    def hide_search_box(self):
        """Hide search box."""
        self._widget.txtSearch.setVisible(False)

    def append_to_history(self, text):
        """Append to history."""
        self._history_model.append_to_history(text)

    def reset(self):
        """Reset module."""
        self._history_model.reset()
        self._model.reset()

    def keyPressEvent(self, e):
        """On Key press event."""
        if e.key() == Qt.Key_F3:
            self._widget.txtSearch.selectAll()
            self._widget.txtSearch.setFocus()

        if e.key() == Qt.Key_Plus:
            self._widget.sLiveFont.setValue(self.live_font + 3)

        if e.key() == Qt.Key_Minus:
            self._widget.sLiveFont.setValue(self.live_font - 3)

        # FIXME
        # if self.__search_in_history:
        #     if e.key() == Qt.Key_PageDown:
        #         self.__next_history_clicked()
        #
        #     if e.key() == Qt.Key_PageUp:
        #         self.__previous_history_clicked()

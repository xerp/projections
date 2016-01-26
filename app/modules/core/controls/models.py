"""Controls model module."""

import os

from PyQt4 import QtGui, QtCore

from app.libraries.modules import AbstractModel, ISearchable
from app.libraries.ui import get_screens_count
from app.libraries.utils import get_image_files, open_directory, is_valid_directory

from app.modules.core import core_modules

from functools import partial


def _remove_buttons_slides(self, cmd_slides):
    """Remove slides buttons."""
    for index in range(0, cmd_slides.count() + 1):
        row, col, rspan, cspan = cmd_slides.getItemPosition(
            index)
        item = cmd_slides.itemAtPosition(row, col)

        if item:
            item.widget().deleteLater()
            del(item)


def _add_elements(parent, elements):
    """Add items to parent."""
    for element in elements:
        parent.addItem(QtGui.QIcon(element),
                       element.split(os.sep)[-1].split('.')[0])
    parent.setIconSize(QtCore.QSize(50, 50))


def _add_buttons_to_panel(panel, rows, cols, button_callback):
    """Add Button to panel."""
    for button_num in range(1, rows + 1):
        button = QtGui.QPushButton(str(button_num))

        button.setMaximumSize(QtCore.QSize(30, 30))
        button.setSizePolicy(QtGui.QSizePolicy.Minimum,
                             QtGui.QSizePolicy.Minimum)

        button.clicked.connect(partial(button_callback, button_num))

        items = panel.count()
        row = items / cols
        col = items % cols

        panel.addWidget(button, row, col)


class HistoryModel(AbstractModel):
    """HistoryModel class."""

    __setters__ = {}

    def _instance_variable(self):
        self._search_in_history = False
        self.__history_control_method = None
        self.__history = {}

    def __setattr__(self, name, value):
        """Set Attributes."""
        if self.__setters__:
            prop = self.__setters__[name]
            prop(value)
        else:
            setattr(AbstractModel, name, value)

    def configure_module(self):
        """Configure module."""
        self.__setters__[
            'history_control_text'] = self.__set_history_control_text

        self.__setters__['search_in_history'] = self.__search_in_history
        self.__setters__['history_control'] = self.__set_history_control

    def __set_history_control_text(self, text):
        pass

    def __search_in_history(self, search):
        """Search in history."""
        self._search_in_history = search

        self._view._widget.cmdPreviousHistory.setVisible(search)
        self._view._widget.cmdNextHistory.setVisible(search)

    def __set_history_control(self, control_method):
        """Set history control."""
        self.__history_control_method = control_method
        self.search_in_history = True

    def clear_history_control(self):
        """Clear history control."""
        if self.__history_control_method:
            self.__history_control_method('')
        else:
            self._view._widget.txtSearch.setText('')

    def next_history_clicked(self):
        """Next history click."""
        option = core_modules.get_toolbox().selected_option()

        if option in self.__history:
            self.__history[option]['position'] += 1
            try:
                position = self.__history[option]['position']
                text = self.__history[option]['data'][position]
                self.set_history_control_text(text)
            except IndexError:
                data = self.__history[option]['data']
                self.__history[option]['position'] = len(data)
                self.clear_history_control()

    def previous_history_clicked(self):
        """Previous history clicked."""
        option = core_modules.get_toolbox().selected_option()

        if option in self.__history:
            if self.__history[option]['position'] > 0:
                self.__history[option]['position'] -= 1
                try:
                    position = self.__history[option]['position']
                    text = self.__history[option]['data'][position]
                    self.set_history_control_text(text)
                except IndexError:
                    self.__history[option]['position'] += 1
            else:
                self.__history[option]['position'] = 0
                position = self.__history[option]['position']
                text = self.__history[option]['data'][position]
                self.__set_history_control_text(text)

    def append_to_history(self, text):
        """Append to History."""
        option = self._toolbox.selected_option()

        if option not in self.__history:
            self.__history[option] = {'position': 0, 'data': []}

        if text and text not in self.__history[option]['data']:
            self.__history[option]['data'].append(text)
            self.__history[option]['position'] = len(
                self.__history[option]['data'])

    def reset(self):
        """Reset model."""
        self.search_in_history = False
        self.__history_control_method = None


class SliderModel(AbstractModel):
    """SliderModel class."""

    def _instance_variable(self):
        self.slide_position = 0

    def __slide_click(self, option):
        """Slide clicked."""
        pass
        # if self._toolbox.selected_module and isinstance(self._toolbox.selected_module, utils.Slideable):
        #     module = self._toolbox.selected_module
        #
        #     self.slide_position = button_num - 1
        #     kwarg = {'item': module.get_projection_item()[self.slide_position],
        #              'font_size': self._widget.sLiveFont.value()}
        #     self._liveViewer.set_text(**kwarg)
        #
        #     self._widget.cmdNext.setEnabled(False if self.slide_position == (
        #         module.get_slide_length() - 1) else True)
        #     self._widget.cmdPrevious.setEnabled(
        #         False if self.slide_position == 0 else True)
        #
        #

    def previous_slide_clicked(self):
        """Previous slide clicked."""
        pass
        # if self._toolbox.selected_module and isinstance(self._toolbox.selected_module, utils.Slideable):
        #     module = self._toolbox.selected_module
        #
        #     self.slide_position -= 1
        #     kwarg = {'item': module.get_projection_item()[self.slide_position],
        #              'font_size': self._widget.sLiveFont.value()}
        #     self._liveViewer.set_text(**kwarg)
        #
        #     self._widget.cmdNext.setEnabled(True)
        #     self._widget.cmdPrevious.setEnabled(
        #         False if self.slide_position == 0 else True)

    def next_slide_clicked(self):
        """Next slide clicked."""
        pass
        # if self._toolbox.selected_module and isinstance(self._toolbox.selected_module, utils.Slideable):
        #     module = self._toolbox.selected_module
        #
        #     self.slide_position += 1
        #     kwarg = {'item': module.get_projection_item()[self.slide_position],
        #              'font_size': self._widget.sLiveFont.value()}
        #     self._liveViewer.set_text(**kwarg)
        #
        #     self._widget.cmdPrevious.setEnabled(True)
        #     self._widget.cmdNext.setEnabled(False if self.slide_position == (
        #         module.get_slide_length() - 1) else True)

    def slider_seeker(self):
        """Slider seeker."""
        pass
        # _remove_buttons_slides(self._view._widget.cmdSlides)
        #
        # self._widget.cmdPrevious.setEnabled(False)
        # self._widget.cmdNext.setEnabled(False)
        #
        # if self._toolbox.in_live and self._toolbox.selected_module.get_slide_length() > 1:
        #     self.__set_buttons_slides(
        #         self._toolbox.selected_module.get_slide_length())
        #
        #     self._widget.cmdPrevious.setEnabled(False)
        #     self._widget.cmdNext.setEnabled(True)

    def set_button_slides(self, max_slides):
        """Set button slides."""
        _remove_buttons_slides(self._view._widget.cmdSlides)
        _add_buttons_to_panel(self._view._widget.cmdSlides,
                              max_slides, 5, self.__slide_click)

    def set_slides(self):
        """Set slides."""
        self.slide_position = 0
        self.slider_seeker()

    def set_enable_slides(self, enable):
        """Set enable slides."""
        self._view._widget.cmdNext.setVisible(enable)
        self._view._widget.cmdPrevious.setVisible(enable)
        self._view._widget.saCmdSlides.setVisible(enable)


class ControlsModel(AbstractModel):
    """ControlsModel class."""

    __getters__ = {}
    __setters__ = {}

    def _instance_variable(self):

        self._module_options_panel = self._view._widget.saModuleOptions

        self.__getters__['selected_image'] = self.__selected_image
        self.__setters__['live'] = self.__set_live

    def __setattr__(self, name, value):
        """Setter methods."""
        if self.__setters__:
            prop = self.__setters__[name]
            prop(value)
        else:
            setattr(AbstractModel, name, value)

    def __getattr__(self, name):
        """Getter methods."""
        if self.__getters__:
            return self.__getters__[name]()
        else:
            return getattr(AbstractModel, name)

    def configure_module(self):
        """Configure Controls module."""
        self._module_options_panel.setVisible(False)
        self._view._widget.txtSearch.setVisible(False)

        self.set_live_screens()

        try:
            self.set_images()
        except Exception, e:
            core_modules.get_status_bar().set_status(e.message, True, 5)

        # FIXME
        # self._view._widget.sLiveFont.setValue(
        #     self.config.getint('LIVE', 'DEFAULT_FONT_SIZE'))

    def __selected_image(self):
        """Return selected image."""
        image_name = str(self._view._widget.cbImagesView.currentText())
        # FIXME
        images = []  # self._view._widget.cbImagesView.images[0]
        if image_name:
            filter_func = lambda img: img.split(
                os.sep)[-1].split('.')[0] == image_name
            return filter(filter_func, images)

    def __set_live(self, in_live):
        """Set in Live."""
        self._view._widget.cbLiveScreens.setEnabled(not in_live)

        if not in_live:
            self._view._widget.cmdPrevious.setEnabled(False)
            self._view._widget.cmdNext.setEnabled(False)

        # selected_module = core_modules.get_toolbox().selected_module
        # if selected_module and isinstance(selected_module, Slideable):
        #     self.slider_seeker()

    def configure_search_box(self, module):
        """Configure search box."""
        self._view._widget.txtSearch.setVisible(True)

        self._view._widget.txtSearch.selectAll()
        self._view._widget.txtSearch.setFocus()

        if module and isinstance(module, ISearchable):
            self._view._callback('search', module.search)

    def set_live_screens(self):
        """Set live screens."""
        screens = get_screens_count()

        self._view._widget.cbLiveScreens.model().clear()
        self._view._widget.cbLiveScreens.addItems(
            map(lambda s: 'Screen {0}'.format(s), range(1, screens + 1)))

        # FIXME
        # if screens >= self.config.getint('LIVE', 'DEFAULT_SCREEN'):
        #     self._view._widget.cbLiveScreens.setCurrentIndex(
        #         self.config.getint('LIVE', 'DEFAULT_SCREEN') - 1)

    def set_images(self):
        """Set images."""
        try:
            self._view._widget.cbImagesView.setInsertPolicy(6)
            # FIXME
            images = get_image_files(self.config.get('GENERAL', 'IMAGES_DIRS'))
            setattr(self._view._widget.cbImagesView, 'images', images)
            _add_elements(self._view._widget.cbImagesView, images)

            try:
                # FIXME
                self._view._widget.cbImagesView.setCurrentIndex(
                    images.index(self.config.get('GENERAL', 'DEFAULT_IMAGE')))
            except Exception:
                pass

        except Exception:
            pass

    def open_images_directory(self):
        """Open image directory."""
        # FIXME
        if self.config.get('GENERAL', 'IMAGES_DIRS'):
            if is_valid_directory(self.config.get('GENERAL', 'IMAGES_DIRS')):
                open_directory(self.config.get('GENERAL', 'IMAGES_DIRS'))
            else:
                core_modules.get_status_bar().set_status(
                    "Image directory doesn't exist", True, time_hide=2)
        else:
            core_modules.get_status_bar().set_status(
                "Image directory property isn't set", True, time_hide=2)

    def reset(self):
        """Reset module."""
        self._view.set_enable_slides(True)
        self._view.enable_live_font = True
        self._view._widget.txtSearch.setVisible(False)
        self._view.search_text = ''

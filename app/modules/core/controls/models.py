"""Controls model module."""

from app.libraries.modules import AbstractModel
from app.libraries.ui import get_screens_count
from app.libraries.utils import get_image_files


class ControlsModel(AbstractModel):

    def configure_module(self):
        self._view._module_options_panel.setVisible(False)
        self._view._widget.txtSearch.setVisible(False)

        self.set_live_screens()

        # try:
        #     self.set_images()
        # except Exception, e:
        #     self._statusbar.set_status(e.message, True, 5)
        #
        # self._view._widget.sLiveFont.setValue(
        #     self.config.getint('LIVE', 'DEFAULT_FONT_SIZE'))

    def set_live_screens(self):
        screens = get_screens_count()

        self._view._widget.cbLiveScreens.model().clear()
        self._view._widget.cbLiveScreens.addItems(
            map(lambda s: 'Screen {0}'.format(s), range(1, screens + 1)))



        # if screens >= self.config.getint('LIVE', 'DEFAULT_SCREEN'):
        #     self._view._widget.cbLiveScreens.setCurrentIndex(
        #         self.config.getint('LIVE', 'DEFAULT_SCREEN') - 1)

    def __remove_buttons_slides(self):
        """Remove slides buttons."""

        for index in range(0, self._view._widget.cmdSlides.count() + 1):
            row, col, rspan, cspan = self._view._widget.cmdSlides.getItemPosition(
                index)
            item = self._view._widget.cmdSlides.itemAtPosition(row, col)

            if item:
                item.widget().deleteLater()
                del (item)

    def set_button_slides(self, max_slides):
        self.__remove_buttons_slides()

        cols = 5
        for slide in range(1, max_slides + 1):
            button = QtGui.QPushButton(str(slide))

            button.setMaximumSize(QtCore.QSize(30, 30))
            button.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                 QtGui.QSizePolicy.Minimum)

            button.clicked.connect(partial(self.__slide_click, slide))

            items = self._widget.cmdSlides.count()
            row = items / cols
            col = items % cols

            self._widget.cmdSlides.addWidget(button, row, col)

    def set_images(self):

        try:
            self._view._widget.cbImagesView.setInsertPolicy(6)
            images = []
            # images = get_image_files(self.config.get('GENERAL', 'IMAGES_DIRS'))
            setattr(self._view._widget.cbImagesView, 'images', images)

            self._view._widget.cbImagesView.model().clear()
            for img in images:
                self._view._widget.cbImagesView.addItem(QtGui.QIcon(
                    img), img.split(os.sep)[-1].split('.')[0])

            self._view._widget.cbImagesView.setIconSize(QtCore.QSize(50, 50))

            try:
                self._view._widget.cbImagesView.setCurrentIndex(
                    images.index(self.config.get('GENERAL', 'DEFAULT_IMAGE')))
            except Exception:
                pass

        except Exception:
            pass

    def open_image_dir(self):
        pass
        # if self.config.get('GENERAL', 'IMAGES_DIRS'):
        #     if is_valid_directory(self.config.get('GENERAL', 'IMAGES_DIRS')):
        #         open_directory(self.config.get('GENERAL', 'IMAGES_DIRS'))
        #     else:
        #         self._statusbar.set_status(
        #             "Image directory doesn't exist", True, time_to_hide=2)
        # else:
        #     self._statusbar.set_status(
        #         "Image directory property isn't set", True, time_to_hide=2)

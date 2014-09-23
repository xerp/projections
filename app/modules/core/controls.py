from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.core.controls as ui_resource
import app.modules.utils as utils

from app.lib.helpers import get_images_view, ImagesViewModel

class Controls(QtGui.QDockWidget,utils.AbstractModule):

    def __init__(self):
        utils.AbstractModule.__init__(self,QtGui.QDockWidget,ui_resource.Ui_projectionsControls())

        self.__set_live_screens()

    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

        self.slides = []
        self.slide_length = len(self.slides)
        self.slide_position = 0

    def config_components(self):
        self._widget.saModuleOptions.setVisible(False)

    def __get_screens(self):
        app = QtGui.QApplication.instance()
        return app.desktop().numScreens()

    def __set_live_screens(self):
        screens = self.__get_screens()

        self._widget.cbLiveScreens.addItems(map(lambda s: 'Screen {0}'.format(s), range(1, screens + 1)))

        if screens >= self.config.getint('LIVE', 'DEFAULT_SCREEN'):
            self._widget.cbLiveScreens.setCurrentIndex(self.config.getint('LIVE', 'DEFAULT_SCREEN') - 1)

    def set_images(self):
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


"""Toolbox core module."""

from PyQt4 import QtGui
# from PyQt4.QtCore import Qt

# import sys
# import os
# import pkgutil
# import importlib

from libraries.modules import CoreModule
import gui

MODULES_TO_EXCLUDE = ['utils', ]


class ToolBox(QtGui.QDockWidget, CoreModule):
    """ToolBox core module class."""

    __controls = {
        'color': {'cmdColorScreen': 'clicked()'},
        'live': {'cmdLive': 'toggled(bool)'},
        'fullscreen': {'cmdFullScreen': 'toggled(bool)'},
        'go_to_live': {'cmdGotoLive': 'clicked()'},
        'direct_live': {'cmdDirectToLive': 'toggled(bool)'},
        'image': {'cmdMainView': 'clicked()'},
        'options': {'cbOptions': 'currentIndexChanged(const QString&)'}
    }

    def __init__(self, parent):
        """Constructor."""
        super(ToolBox, self).__init__(parent, QtGui.QDockWidget,
                                      gui.Ui_dockProjectionsTools(),
                                      self.__controls)

    def _instance_variable(self):
        super(ToolBox, self)._instance_variable()

        self.in_live = False
        self.direct_live = False

    def _configure(self):
        # self._widget.cmdColorScreen.setText('{0} (F9)'.format(
        #     self.config.get('LIVE', 'DEFAULT_COLOR').upper()))
        # self._widget.cmdColorScreen.setShortcut('F9')
        # self._widget.cmdFullScreen.setVisible(False)

        # FIXME self.__set_modules()

        self.callback('live', self.set_live)
        self.callback('image', self.__image_view)
        self.callback('color', self.__color_view)
        self.callback('options', self.__option_changed)
        self.callback('direct_live', self.__direct_to_live)
        self.callback('go_to_live', self.go_to_live)

# def __set_modules(self):
# modules = filter(lambda mod: 'app.modules.' in mod and 'core' not in mod,
#                  map(lambda (m, n, i): n, pkgutil.walk_packages('app.modules')))
# modules = map(lambda mod: mod.split('.')[-1].capitalize(), modules)
#
# try:
#     MODULES_TO_EXCLUDE_TEMP = MODULES_TO_EXCLUDE + \
#         self.config.get('GENERAL', 'options_to_exclude').split(',')
#     modules = filter(lambda mod: mod.lower()
#                      not in MODULES_TO_EXCLUDE_TEMP, modules)
# except Exception:
#     modules = filter(lambda mod: mod.lower()
#                      not in MODULES_TO_EXCLUDE, modules)
#
# modules = map(lambda m: m.replace('_', ' '), modules)
#
# # Ignore bible module on Windows
# if sys.platform == 'win32':
#     filter_func = lambda mo: not mo.lower() == 'bible'
#     modules = filter(filter_func, modules)
#
# self._widget.cbOptions.addItems(modules)
#
# try:
#     indexDefaultOption = modules.index(self.config.get(
#         'GENERAL', 'default_option').capitalize())
#     self._widget.cbOptions.setCurrentIndex(indexDefaultOption)
# except Exception:
#     pass

    def __image_view(self):
        pass
        # FIXME
        # try:
        #     self._liveViewer.set_image(self._controls.selected_image())
        #
        #     self._statusbar.set_button_status('Image View')
        #     self._statusbar.set_status('Live in Image View')
        #
        # except utils.ProjectionError, e:
        #     self._statusbar.set_status(e.message, True, 5)

    def __color_view(self):
        pass
        # FIXME
        # self._liveViewer.set_color()
        #
        # color = self.config.get('LIVE', 'DEFAULT_COLOR').upper()
        # self._statusbar.set_button_status(color)
        # self._statusbar.set_status('Live in {0}'.format(color))

    def __full_screen(self, active):
        pass
        # FIXME
        # self._liveViewer.set_full_screen(active)
        # self._statusbar.set_full_screen_status(active)

    def __option_changed(self, text):
        self.configure_selected_module()

    def __direct_to_live(self, active):
        self.direct_live = active
        self._statusbar.set_status(
            'Direct live {0}'.format('on' if active else 'off'))

    def go_to_live(self):
        pass
        # preview_text = self._previewer.toPlainText()
        # module = self.selected_module
        #
        # if module and isinstance(module, utils.Projectable):
        #     module.process_projection(preview_text)
        #
        #     kwargs = {'item': module.get_projection_item(),
        #               'font_size': self._controls.live_font()}
        #     getattr(self._liveViewer, 'set_{0}'.format(
        #         module.get_projection_method()))(**kwargs)
        #
        # elif module and isinstance(module, utils.Slideable):
        #     try:
        #         kwargs = {'item': module.get_projection_item()[self._controls.slide_position],
        #                   'font_size': self._controls.live_font()}
        #         self._liveViewer.set_text(**kwargs)
        #         self._controls.seeker()
        #     except IndexError:
        #         pass
        #
        # self._statusbar.set_status('View refreshed')

    def reset(self):
        pass

    def configure_selected_module(self):
        pass
        # module = self.selected_option()
        # if module:
        #     module = module.replace(' ', '_')
        #     module = importlib.import_module(
        #         'app.modules.{0}'.format(str(module).lower()))
        #
        #     self.selected_module = None
        #     if hasattr(module, 'configure_options'):
        #         self._controls.reset()
        #         self._previewer.reset()
        #         self.reset()
        #         self.selected_module = module.configure_options(
        #             controls=self._controls,
        #             statusbar=self._statusbar,
        #             previewer=self._previewer,
        #             liveViewer=self._liveViewer,
        #             toolbox=self)
        #     else:
        #         self._controls.hide_module_options()
        #         self._controls.hide_search_box()
        #         self._statusbar.set_status(
        #             '{0} module dont have options'.format(
        #                 module.__name__.split('.')[-1].replace('_', ' ')),
        #             time_to_hide=5)

    def selected_option(self):
        return str(self._widget.cbOptions.currentText())

    def set_live(self, in_live):
        pass
        # self.in_live = in_live
        #
        # self._widget.cmdFullScreen.setChecked(False)
        # self._widget.cmdDirectToLive.setChecked(False)
        #
        # self._widget.cmdDirectToLive.setEnabled(in_live)
        # self._widget.cmdGotoLive.setEnabled(in_live)
        # self._widget.cmdMainView.setEnabled(in_live)
        # self._widget.cmdColorScreen.setEnabled(in_live)
        # self._widget.cmdFullScreen.setEnabled(in_live)
        #
        # self._widget.cmdLive.setChecked(in_live)
        #
        # self._statusbar.set_live(in_live)
        # self._controls.set_live(in_live)
        #
        # self._liveViewer.set_visible(
        #     self.in_live, self._controls.selected_screen())
        # self._liveViewer.set_color(Qt.red)

"""ToolBox model module."""

# from PyQt4.QtCore import Qt

# import sys
# import os
# import pkgutil
# import importlib

from app.libraries.modules import AbstractModel
from app.libraries.utils import ProjectionError
from app.modules.core import core_modules


def __get_modules():
    """Return a list of modules."""
    # modules = filter(lambda mod: 'app.modules.' in mod and 'core' not in mod,
    #                  map(lambda (m, n, i): n, pkgutil.walk_packages('app.modules')))
    # modules = map(lambda mod: mod.split('.')[-1].capitalize(), modules)
    pass


class ToolBoxModel(AbstractModel):
    """ToolBoxModel class."""

    def _instance_variable(self):
        self.in_live = False
        self.direct_live = False

    def configure_module(self):
        """Configure module."""
        # self._widget.cmdColorScreen.setText('{0} (F9)'.format(
        #     self.config.get('LIVE', 'DEFAULT_COLOR').upper()))
        # self._widget.cmdColorScreen.setShortcut('F9')
        # self._widget.cmdFullScreen.setVisible(False)
        pass

    def image_view(self):
        """Image view option."""
        try:
            core_modules.get_live_viewer().set_image(
                core_modules.get_controls().selected_image())

            core_modules.get_status_bar().set_button_status('Image View')
            core_modules.get_status_bar().set_status('Live in Image View')

        except ProjectionError, e:
            core_modules.get_status_bar().set_status(e.message, True, 5)

    def color_view(self):
        """Color view option."""
        core_modules.get_live_viewer().set_color()

        color = 'BLACK'  # self.config.get('LIVE', 'DEFAULT_COLOR').upper()
        core_modules.get_status_bar().set_button_status(color)
        core_modules.get_status_bar().set_status(
            'Live in {0} color'.format(color))

    def fullscreen(self, active):
        """Fullscreen option."""
        core_modules.get_live_viewer().set_full_screen(active)
        core_modules.get_status_bar().set_full_screen_status(active)

    def direct_to_live(self, active):
        """Direct to live option."""
        self.direct_live = active
        core_modules.get_status_bar().set_status(
            'Direct live {0}'.format('on' if active else 'off'))

    def go_to_live(self):
        """Go to Live option."""
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
        #
        #

    def set_live(self, in_live):
        """
            Set in live.

        Parameters:
            * in_live
        """
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

    def configure_selected_module(self):
        """Configure selected module."""
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

    def set_modules(self):
        """Set module."""
        # modules = __get_modules()
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

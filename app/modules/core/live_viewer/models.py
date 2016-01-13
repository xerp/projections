"""Live viewer models module."""

import os

from PyQt4 import QtGui
from PyQt4.QtCore import QUrl

from jinja2 import Template

from app.libraries.modules import AbstractModel
from app.libraries.encoding import get_default_encoding
from app.libraries.utils import ProjectionError
from app.libraries.configuration import get_user_app_directory
from app.libraries.encoding import to_str


__ZOOM_OUT_STEP = 8
__VIEWER_FILE = os.path.join(get_user_app_directory(), 'last_live.html')


def _create_viewer_file(unicode_html):
    """Create Live viewer html file."""
    with open(__VIEWER_FILE, "w") as file:
        file.write(to_str(unicode_html, 'latin1'))


def _get_screen_geometry(screen):
    """Return screen geometry."""
    return QtGui.QApplication.instance().desktop().screenGeometry(screen)


def _get_image_html_view():
    """Return image html view."""
    return '''
            <body>
                <style>
                    body{
                        background-color:black;
                    }
                    img{
                        background: no-repeat;
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                        vertical-align: middle;
                        width:98%;
                        height:98%;
                    }
                </style>
                <img src="{{image}}">
            </body>
    '''


def _get_color_html_view():
    """Return color html view."""
    return '<body style="background-color:{{color}}"></body>'


def _set_html_text(lblLive):
    lblLive.load(QUrl.fromLocalFile(__VIEWER_FILE))


class LiveViewerModel(AbstractModel):
    """LiveViewerModel class."""

    def __init__(self, view):
        """LiveViewerModel Constructor."""
        AbstractModel.__init__(self, view)

    def _instance_variable(self):
        self.__screen_geometry = None

    def set_visible(self, visible, screen):
        """
            Set Visible.

        Parameters:
            * visible: visible or not
            * screen: screen number
        """
        self.__screen_geometry = _get_screen_geometry(screen)

        geometry = self._view.geometry()
        geometry.setX(self.__screen_geometry.x())
        geometry.setY(self.__screen_geometry.y())
        self._view.setGeometry(geometry)

        self._view.reset()
        self._view.show() if visible else self._view.hide()
        self._view.setFixedSize(self.__screen_geometry.size())

    def reset(self, default_size):
        """
            Reset view.

        Parameters:
            * default_size: default size
        """
        self._view.set_full_screen(False)
        self._view.setFixedSize(default_size)

    def set_full_screen(self, full_screen, default_size):
        """
            Set Full screen.

        Parameters:
            * full_screen
            * default_size
        """
        try:
            self._view.setFixedSize(self.__screen_geometry.size()
                                    if full_screen else default_size)
        except Exception:
            raise ProjectionError('window must be visible before full_screen')

    def set_color(self, color, lblLive):
        """
            Set color.

        Parameters:
            * color
            * lblLive
        """
        # color = self.config.get(
        #     'LIVE', 'DEFAULT_COLOR') if not color else color

        template = Template(_get_color_html_view())
        lblLive.setHtml(template.render(color=color))

    def set_image(self, image_file, lblLive):
        """
            Set Image.

        Parameters:
            * image_file
            * lblLive
        """
        self._view.set_color()

        if not image_file:
            raise ProjectionError('error occurred trying to loading image')

        template = Template(_get_image_html_view())
        _create_viewer_file(template.render(image=image_file))
        _set_html_text(lblLive)

    def set_text(self, lblLive, **kwargs):
        """
            Set text.

        Parameters:
            * lblLive
            * kwargs: dictionary with multiple variables
        """
        self._view.set_color()

        unicode_last_template = Template(kwargs['item'])
        font_size = kwargs['font_size']
        unicode_html_text = unicode_last_template.render(
            charset=get_default_encoding,
            font_size=font_size if font_size > 0 else __ZOOM_OUT_STEP)

        _create_viewer_file(unicode_html_text)
        _set_html_text(lblLive)

    def set_url(self, lblLive, **kwargs):
        """
            Set URL.

        Parameters:
            * lblLive
            * kwargs: dictionary with multiple variables
        """
        if kwargs['item']:
            lblLive.load(QUrl(kwargs['item']))

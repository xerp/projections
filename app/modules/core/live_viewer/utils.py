"""Live viewer utils module."""

import os

from libraries.configuration import get_user_app_directory
from libraries.encoding import to_str
from PyQt4 import QtGui

ZOOM_OUT_STEP = 8


def get_viewer_file_path():
    """Return viewer file path."""
    return os.path.join(get_user_app_directory(), 'last_live.html')


def create_viewer_file(unicode_html):
    """Create Live viewer html file."""
    with open(get_viewer_file_path(), "w") as file:
        file.write(to_str(unicode_html, 'latin1'))


def get_screen_geometry(screen):
    """Return screen geometry."""
    return QtGui.QApplication.instance().screenGeometry(screen)


def get_image_html_view():
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

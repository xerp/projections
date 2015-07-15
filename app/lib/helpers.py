import os
import sys
import subprocess
from ConfigParser import ConfigParser

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

conf = ConfigParser()
conf.read('config.ini')


def get_default_encoding(pretty=False):
    return 'UTF-8' if pretty else 'utf8'


def to_unicode(text, encoding=get_default_encoding(), errors='strict'):
    return unicode(text, encoding, errors)


def to_str(text, encoding=get_default_encoding(), errors='strict'):
    return str(text.encode(encoding, errors))


def get_user_name_home():
    return os.path.expanduser('~')


def get_user_app_directory():
    user_name_home = get_user_name_home()
    dir = ''

    # Windows
    if sys.platform == 'win32':
        dir = os.path.join(user_name_home, 'AppData\\Local\\Projections')
    # Linux
    elif sys.platform == 'linux2':
        dir = os.path.join(user_name_home, '.local/share/projections')

    if dir and not os.path.isdir(dir):
        os.mkdir(dir)

    return dir


def get_app_config_filename():
    return os.path.join(get_user_app_directory(), 'app_config.ini')


def get_user_app_config():
    filename = get_app_config_filename()
    if filename and os.path.isfile(filename):
        config = ConfigParser()
        config.read(filename)
        return config


def get_user_application_geometry():
    # Default Geometry
    geometry = {'x': 50,
                'y': 50,
                'width': 900,
                'height': 600}

    config = get_user_app_config()
    if config:
        try:
            geometry['x'] = config.getfloat('LOCATION', 'x')
            geometry['y'] = config.getfloat('LOCATION', 'y')
            geometry['width'] = config.getfloat('SIZE', 'width')
            geometry['height'] = config.getfloat('SIZE', 'height')
        except Exception:
            pass

    return geometry


def set_user_configuration(filename, kwargs):
    with open(filename, 'w') as cfg_file:
        config = ConfigParser()

        for section in kwargs.keys():
            config.add_section(section)

            for variable in kwargs[section].keys():
                config.set(section, variable, kwargs[section][variable])

        config.write(cfg_file)


def set_user_application_geometry(geometry):
    filename = get_app_config_filename()

    config = {'LOCATION': {'x': geometry.x(), 'y': geometry.y()},
              'SIZE': {'width': geometry.width(), 'height': geometry.height()}}

    set_user_configuration(filename, config)


def is_valid_directory(dir):
    return os.path.isdir(dir)


def open_directory(dir):
    # Windows
    if sys.platform == 'win32':
        subprocess.Popen(['explorer', dir])

    # On Mac
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', dir])

    # Linux
    else:
        subprocess.Popen(['xdg-open', dir])


def remove_pycs():
    for root, dirs, files in os.walk('.'):
        for fi in files:
            if fi[-3:] == 'pyc':
                os.remove(os.path.join(root, fi))


def get_projections_font(font_properties):
    font = QtGui.QFont(font_properties.get('name', 'arial'))
    font.setPointSize(int(font_properties.get('size', conf.getint('LIVE', 'DEFAULT_FONT_SIZE'))))
    font.setBold(bool(font_properties.get('bold', False)))
    font.setWeight(int(font_properties.get('weight', 75)))

    return font


def get_screens():
    app = QtGui.QApplication.instance()
    return app.desktop().numScreens()


def get_images_view(directories=conf.get('GENERAL', 'IMAGES_DIRS')):
    directories = directories.split(',')
    images_views = []
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            images_views.extend(
                map(lambda f: os.path.join(root, f), filter(lambda f: f.endswith('.png') or f.endswith('.jpg'), files)))

    return images_views


def set_alignment(text_edit, desired_alignment):
    #Make sure the cursor is at the start of the text field
    text_edit.moveCursor(QtGui.QTextCursor.Start)

    last_position = -1
    curr_position = text_edit.textCursor().position()

    while last_position != curr_position:
        text_edit.setAlignment(desired_alignment)
        text_edit.moveCursor(QtGui.QTextCursor.Down)
        last_position = curr_position
        curr_position = text_edit.textCursor().position()

    #Move to the end of the text field in preparation for whatever comes next
    text_edit.moveCursor(QtGui.QTextCursor.End)


class AbstractProjectionLinealDataModel(QtCore.QAbstractListModel):
    def __init__(self, data_list=[], parent=None):
        QtCore.QAbstractListModel.__init__(self, None)

        self.__parent = parent
        self.data_list = data_list

    def parent(self, *args, **kwargs):
        return self.__parent

    def rowCount(self, parent=QtCore.QModelIndex):
        return len(self.data_list)

    def selected(self):
        try:
            return self.data_list[self.parent().currentIndex()]
        except (AttributeError, IndexError):
            pass


class ImagesViewModel(AbstractProjectionLinealDataModel):
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            image = self.data_list[index.row()]

            if role == Qt.DisplayRole:
                print 'gh'
            elif role == Qt.DecorationRole:
                return QtGui.QIcon(image)

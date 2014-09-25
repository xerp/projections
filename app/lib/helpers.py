import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

import app.modules.songs as songs
from ConfigParser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')


def remove_pycs():
    for root,dirs,files in os.walk('.'):
        for fi in files:
            if fi[-3:] == 'pyc':
                os.remove(os.path.join(root,fi))

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


# def get_songs_completer(txt_search):
#     so = songs.get_songs()

#     completer = QtGui.QCompleter(txt_search)
#     completer.setModel(SongsDataModel(so, completer))
#     completer.setCaseSensitivity(Qt.CaseInsensitive)
#     completer.setCompletionRole(Qt.DisplayRole)

#     completer.popup().setStyleSheet("background-color: red;color:white")

#     return completer


# def artists_model(cb_artist):
#     artists = songs.get_artists()

#     model = ArtistDataModel(artists, cb_artist)
#     cb_artist.setModel(model)

#     return model


# def set_alignment(text_edit, desired_alignment):
#     #Make sure the cursor is at the start of the text field
#     text_edit.moveCursor(QtGui.QTextCursor.Start)

#     last_position = -1
#     curr_position = text_edit.textCursor().position()

#     while last_position != curr_position:
#         text_edit.setAlignment(desired_alignment)
#         text_edit.moveCursor(QtGui.QTextCursor.Down)
#         last_position = curr_position
#         curr_position = text_edit.textCursor().position()

#     #Move to the end of the text field in preparation for whatever comes next
#     text_edit.moveCursor(QtGui.QTextCursor.End)


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
        except (AttributeError,IndexError):
            pass

class ImagesViewModel(AbstractProjectionLinealDataModel):
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            image = self.data_list[index.row()]

            return image.split(os.sep)[-1].split('.')[0]


# class ArtistDataModel(AbstractProjectionLinealDataModel):
#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid() and role == Qt.DisplayRole:
#             artist = self.data_list[index.row()]

#             return artist.full_name


# class SongsDataModel(AbstractProjectionLinealDataModel):
#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid() and role == Qt.DisplayRole:
#             song = self.data_list[index.row()]

#             try:
#                 return song.title_and_artist
#             except Exception:
#                 pass

#     def selected(self):
#         text = self.parent().parent().text()

#         try:
#             return filter(lambda s: s.title_and_artist == text, self.data_list)[0]
#         except (TypeError, IndexError):
#             raise songs.SongError('song not found')
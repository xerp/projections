from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.lib.orm as orm
import app.resources.modules.karaoke.options as ui_opts_resource
import app.resources.modules.karaoke.management as ui_manage_resource
import app.modules.utils as utils

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import or_
from sqlalchemy.orm import relationship
from ConfigParser import ConfigParser


DELIMITER = '\n\n'

def configure_options(**kwargs):
    options = KaraokeOptions(kwargs['controls'].module_options_panel)
    options.set_dependents(kwargs)
    options.configure()

    return options

class SongError(Exception):
    pass


class KaraokeOptions(utils.ApplicationModule):

    __controls = {
        'add_song':{'cmdAddSong':'clicked()'},
        'delete_song':{'cmdDeleteSong':'clicked()'},
        'edit_song':{'cmdEditSong':'clicked()'},
        'song_selected':{'lstSongs':'itemClicked (QTableWidgetItem*)'},
        'show_song':{'lstSongs':'itemDoubleClicked (QTableWidgetItem*)'}
    }

    def __init__(self,parent):
        utils.ApplicationModule.__init__(self,parent,None,ui_opts_resource.Ui_options(),self.__controls)
        self.__ADAPTER = orm.Adapter(self.config.get('GENERAL', 'DB_PATH'), orm.SQLITE)

    def config_components(self):

        #Table configuration
        self._widget.lstSongs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._widget.lstSongs.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self._widget.lstSongs.clear()
        self._widget.lstSongs.hideColumn(0)
        self._widget.lstSongs.hideColumn(1)
        self._widget.lstSongs.hideColumn(2)


        self.callback('add_song',self.__add_song)
        self.callback('delete_song',self.__delete_song)
        self.callback('edit_song',self.__edit_song)
        self.callback('song_selected',self.__song_selected)
        self.callback('show_song',self.__show_song)

    def configure(self):

        self._controls.add_module_options(self)
        self._controls.configure_search_box(self.__search_song)

        self._statusbar.set_status('Song module loaded successfully')


    def keyPressEvent(self, e):
        
        if e.key() in [Qt.Key_Enter,Qt.Key_Return]:
            item = self._widget.lstSongs.currentItem()

            if item:
                self.__show_song(item)

    def __set_table_data(self,songs):

        def __set_row(*cells):
            row = self._widget.lstSongs.rowCount()
            self._widget.lstSongs.insertRow(row)

            for cell in cells:
                self._widget.lstSongs.setItem(row,cell.column,cell)

        self._widget.lstSongs.setRowCount(0)
        if songs:
            for song in songs:
                __set_row(
                    SongTableRow(0,song.id),
                    SongTableRow(1,song.title),
                    SongTableRow(2,song.artist.full_name))

            self._widget.lstSongs.showColumn(1)
            self._widget.lstSongs.showColumn(2)

            self._widget.lstSongs.resizeColumnsToContents()
        else:
            self._widget.lstSongs.hideColumn(1)
            self._widget.lstSongs.hideColumn(2)

    def __search_song(self):
        search_text = self._controls.search_box_text()

        songs = self.__songs_db(search_text)
        self.__set_table_data(songs)

        self._controls.clear_search_box()

    def __add_song(self):
        songManagement = SongManagement(self,'Add Song')
        songManagement.show()

    def __edit_song(self):
        idItem = self._widget.lstSongs.item(self._widget.lstSongs.currentItem().row(),0)

        songManagement = SongManagement(self,'Edit Song',self.__song_db(int(idItem.text())))
        songManagement.show()

    def __delete_song(self):
        idItem = self._widget.lstSongs.item(self._widget.lstSongs.currentItem().row(),0)

        self.__delete_song_db(int(idItem.text()))
        self._widget.lstSongs.removeRow(self._widget.lstSongs.currentItem().row())

        self._widget.cmdEditSong.setEnabled(False)
        self._widget.cmdDeleteSong.setEnabled(False)

    def __song_selected(self,item):

        self._widget.cmdEditSong.setEnabled(True)
        self._widget.cmdDeleteSong.setEnabled(True)

    def __show_song(self,item):
        idItem = self._widget.lstSongs.item(item.row(),0)

        song = self.__song_db(int(idItem.text()))
        self._previewer.set_text(song.body)

    def __songs_db(self,criteria):
        query, session = self.__ADAPTER.get_query(Song)

        query = query.join(Song.artist).filter(
            (Artist.first_name.like('%{0}%'.format(criteria)))
            | (Artist.last_name.like('%{0}%'.format(criteria)))
            | (Song.title.like('%{0}%'.format(criteria)))
            | (Song.body.like('%{0}%'.format(criteria))))

        return query.all()

    def __song_db(self,idSong):
        query, session = self.__ADAPTER.get_query(Song)

        song =  query.filter(Song.id == idSong).one()
        session.merge(song.artist, load=True)
        session.close()

        return song

    def __delete_song_db(self,idSong):
        query, session = self.__ADAPTER.get_query(Song)

        song = query.filter(Song.id == idSong).one()

        session.delete(song)
        session.commit()
        session.close()

        return True


class SongManagement(QtGui.QWizard,utils.ApplicationModule):

    def __init__(self,parent,title,song = None):
        self.__windowTitle = title
        self.__song = song;
        utils.ApplicationModule.__init__(self,parent,QtGui.QWizard,ui_manage_resource.Ui_songManagement())

    def config_components(self):
        self.setWindowTitle(self.__windowTitle)

        #Song Configure
        if self.__song:
            self.setWindowTitle('{0} - ({1})'.format(self.__windowTitle, self.__song.title_and_artist))

            self._widget.txtTitle.setText(self.__song.title)
            self._widget.txtSongBody.setText(self.__song.body)


class SongTableRow(QtGui.QTableWidgetItem):

    def __init__(self,column,songPropertyValue):
        QtGui.QTableWidgetItem.__init__(self,str(songPropertyValue))

        self.setFlags(QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsEnabled)
        self.column = column

    def __repr__(self):
        return '<%s>' % self.text()


class Artist(orm.BaseTable):
    __tablename__ = 'Artist'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    songs = relationship("Song", backref="Artist")

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name if self.last_name else self.first_name

    def __repr__(self):
        return '<%s>' % self.full_name


class Song(orm.BaseTable):
    __tablename__ = 'Song'

    id = Column(Integer, primary_key=True)
    __id_artist = Column('id_artist', Integer, ForeignKey('Artist.id'))
    artist = relationship('Artist')
    title = Column(String(100))
    body = Column(Text)

    @property
    def title_and_artist(self):
        return '{title} - {artist}'.format(title=self.title, artist=self.artist.full_name)

    def __repr__(self):
        return self.title_and_artist


# def artist_exist(artist, edit=False):
#     query, session = __ADAPTER.get_query(Artist)

#     query = query.filter(Artist.first_name == artist.first_name)

#     if artist.last_name:
#         query = query.filter(Artist.last_name == artist.last_name)

#     if edit:
#         query = query.filter(Artist.id != artist.id)

#     artists = query.all()

#     return len(artists) != 0


# def song_exist(song, edit=False):
#     query, session = __ADAPTER.get_query(Song)

#     query = query.filter(Song.title == song.title)

#     if song.artist:
#         query = query.filter(
#             Artist.first_name == song.artist.first_name,
#             Artist.last_name == song.artist.last_name,
#         )

#     if edit:
#         query = query.filter(Song.id != song.id)

#     songs = query.all()

#     return len(songs) != 0


# def artist_has_song(artist):
#     query, session = __ADAPTER.get_query(Song)

#     query = query.join(Artist).filter(Artist.id == artist.id)

#     songs = query.all()

#     return len(songs) != 0


# def insert_song(song):
#     if not song.title or not song.body or not song.artist:
#         raise SongError('title, artist and body of song are required')

#     song.title = song.title.capitalize()
#     song.body = song.body.upper()

#     if song_exist(song):
#         raise SongError('song already exist')

#     query, session = __ADAPTER.get_query(Song)

#     session.merge(song.artist, load=False)
#     session.add(song)
#     session.commit()

#     return True


# def edit_song(song):
#     if not song.title or not song.body or not song.artist:
#         raise SongError('title, artist and body of song are required')

#     song_to_edit, session = __ADAPTER.get(Song, song.id)

#     song_to_edit.title = song.title.capitalize()
#     song_to_edit.body = song.body.upper()

#     if song_exist(song, True):
#         raise SongError('song already exist')

#     session.commit()

#     return True


# def delete_song(song):
#     song, session = __ADAPTER.get(Song, song.id)

#     session.delete(song)
#     session.commit()

#     return True


# def insert_artist(artist):
#     if not artist.first_name:
#         raise SongError('first name of artist are required')

#     artist.first_name = artist.first_name.capitalize()

#     if artist.last_name:
#         artist.last_name = artist.last_name.capitalize()

#     if artist_exist(artist):
#         raise SongError('artist already exist')

#     query, session = __ADAPTER.get_query(Artist)

#     session.add(artist)
#     session.commit()

#     return True


# def edit_artist(artist):
#     if not artist.first_name:
#         raise SongError('first name of artist are required')

#     artist_to_edit, session = __ADAPTER.get(Artist, artist.id)

#     artist_to_edit.first_name = artist.first_name.capitalize()

#     if artist.last_name:
#         artist_to_edit.last_name = artist.last_name.capitalize()

#     if artist_exist(artist, True):
#         raise SongError('artist already exist')

#     session.commit()

#     return True

# def delete_artist(artist):
#     artist, session = __ADAPTER.get(Artist, artist.id)

#     if artist_has_song(artist):
#         raise SongError('cant delete artist, has songs associated')

#     session.delete(artist)
#     session.commit()

#     return True

#     selected_song = None
#     def cmdAddSong_clicked(self):

#         try:
#             a_song = SongManagement(self, 'Add Song')
#             a_song.exec_()

#             completer = get_songs_completer(self.__window.txtSearch)
#             self.__window.txtSearch.setCompleter(completer)
#             self.__window.txtSearch.setFocus()

#             self.set_status('Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

#         except songs.SongError, e:
#             self.set_status(str(e), True)

#     def cmdEditSong_clicked(self):
#         try:
#             a_song = SongManagement(self, 'Edit Song')
#             a_song.set_song(self.selected_song)
#             a_song.exec_()

#             self.__window.txtPreview.clear()
#             self.__window.txtSearch.clear()

#             completer = get_songs_completer(self.__window.txtSearch)
#             self.__window.txtSearch.setCompleter(completer)
#             self.__window.txtSearch.setFocus()

#             self.__window.cmdEditSong.setEnabled(False)
#             self.__window.cmdDeleteSong.setEnabled(False)

#             self.selected_song = None

#             self.set_status('Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

#         except songs.SongError, e:
#             self.set_status(str(e), True)


#     def cmdDeleteSong_clicked(self):

#         self.selected_song = self.__window.txtSearch.completer().model().selected()
#         songs.delete_song(self.selected_song)
#         self.selected_song = None

#         self.__window.txtPreview.clear()
#         self.__window.txtSearch.clear()

#         completer = get_songs_completer(self.__window.txtSearch)
#         self.__window.txtSearch.setCompleter(completer)
#         self.__window.txtSearch.setFocus()

#         self.__window.cmdEditSong.setEnabled(False)
#         self.__window.cmdDeleteSong.setEnabled(False)

#         self.set_status('Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

#     def rbSong_clicked(self):
#         self.__window.txtSearch.setPlaceholderText('Search a song (F3)')

#         try:
#             completer = get_songs_completer(self.__window.txtSearch)
#             self.__window.txtSearch.setCompleter(completer)

#             self.set_status(
#                 'Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

#         except songs.SongError:
#             self.set_status('One error occurred try loading songs', True)

#         self.__window.txtSearch.selectAll()
#         self.__window.txtSearch.setFocus()


# class SongManagement(QtGui.QDialog):
#     SONG_ADD_MODE = 0
#     SONG_EDIT_MODE = 1
#     __edited_artist = None
#     __song = None

#     def __init__(self, parent, title, mode=SONG_ADD_MODE):
#         QtGui.QDialog.__init__(self, parent, Qt.Tool)
#         self.__window = song_manage.Ui_frmSongManagement()
#         self.__window.setupUi(self)
#         self.setWindowTitle(title)

#         self.mode = mode
#         self.set_handlers()
#         self.window_config()

#         self.set_status('Ready')

#     def set_handlers(self):

#         self.__window.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.cmdSave_clicked)
#         self.__window.cmdAddArtist.clicked.connect(self.cmdAddArtist_clicked)
#         self.__window.cmdEditArtist.clicked.connect(self.cmdEditArtist_clicked)
#         self.__window.cmdDeleteArtist.clicked.connect(self.cmdDeleteArtist_clicked)

#     def window_config(self):

#         self.txtBody = SongBody(self)

#         font = get_projections_font(dict(conf.items('FONT_LIVE')))
#         font.setPointSize(conf.getint('SONG', 'MANAGEMENT_FONT_SIZE'))
#         self.txtBody.setFont(font)

#         set_alignment(self.txtBody, Qt.AlignCenter)
#         self.txtBody.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#         self.txtBody.setAcceptRichText(False)
#         self.setTabOrder(self.__window.cbArtist, self.txtBody)
#         self.__window.verticalLayout.insertWidget(1, self.txtBody)

#         artists_model(self.__window.cbArtist)
#         self.__window.txtTitle.setFocus()

#     def set_status(self, status, error=False):
#         self.__window.lblStatus.setText(status.capitalize())

#     def set_song(self, song):

#         if not song:
#             raise songs.SongError('Non song selected')

#         self.mode = self.SONG_EDIT_MODE
#         self.__song = song

#         self.__window.txtTitle.setText(song.title)
#         self.txtBody.setText(song.body)
#         set_alignment(self.txtBody, Qt.AlignCenter)

#     def cmdSave_clicked(self):
#         song = songs.Song() if self.mode == self.SONG_ADD_MODE else self.__song

#         song.title = unicode(self.__window.txtTitle.text().toUtf8(), 'utf-8')
#         song.body = unicode(self.txtBody.toPlainText().toUtf8(), 'utf-8')

#         try:
#             song.artist = self.__window.cbArtist.model().selected()
#         except AssertionError:
#             pass

#         try:
#             if self.mode == self.SONG_ADD_MODE:
#                 songs.insert_song(song)
#             else:
#                 songs.edit_song(song)

#             self.hide()
#         except songs.SongError, e:
#             self.set_status(str(e))

#     def cmdAddArtist_clicked(self):

#         text, accept = QtGui.QInputDialog.getText(QtGui.QInputDialog(), 'Add Artist', 'Artist', QtGui.QLineEdit.Normal)

#         if accept and text:
#             values = text.split(',')
#             artist = songs.Artist()

#             artist.first_name = str(values[0])
#             try:
#                 artist.last_name = str(values[1])
#             except IndexError:
#                 pass

#             try:
#                 songs.insert_artist(artist)
#                 artists_model(self.__window.cbArtist)
#             except songs.SongError, e:
#                 self.set_status(str(e), True)

#     def cmdEditArtist_clicked(self):
#         artist = self.__window.cbArtist.model().selected()

#         text, accept = QtGui.QInputDialog.getText(QtGui.QInputDialog(), 'Edit Artist', 'Artist',
#                                                   QtGui.QLineEdit.Normal,
#                                                   '{0},{1}'.format(artist.first_name, artist.last_name))

#         if accept and text:
#             values = text.split(',')

#             artist.first_name = str(values[0]).strip(' ')
#             try:
#                 artist.last_name = str(values[1]).strip(' ')
#             except IndexError:
#                 pass

#             try:
#                 songs.edit_artist(artist)
#                 artists_model(self.__window.cbArtist)
#             except songs.SongError, e:
#                 self.set_status(str(e), True)

#     def cmdDeleteArtist_clicked(self):
#         artist = self.__window.cbArtist.model().selected()

#         try:
#             songs.delete_artist(artist)
#             artists_model(self.__window.cbArtist)
#         except songs.SongError, e:
#             self.set_status(str(e), True)
import app.lib.orm as orm

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ConfigParser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')

__ADAPTER = orm.Adapter(conf.get('SONG', 'DB_PATH'), orm.SQLITE)
DELIMITER = '\n\n'


class Artist(orm.BaseTable):
    __tablename__ = 'Artist'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    songs = relationship("Song", backref="Artist")

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name if self.last_name else self.first_name


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


class SongError(Exception):
    pass


def get_songs(title=None):
    query, session = __ADAPTER.get_query(Song)

    if title:
        query = query.filter(Song.title.like('%{0}%'.format(title)))

    return query.all()


def get_artists():
    query, session = __ADAPTER.get_query(Artist)

    return query.all()


def artist_exist(artist, edit=False):
    query, session = __ADAPTER.get_query(Artist)

    query = query.filter(Artist.first_name == artist.first_name)

    if artist.last_name:
        query = query.filter(Artist.last_name == artist.last_name)

    if edit:
        query = query.filter(Artist.id != artist.id)

    artists = query.all()

    return len(artists) != 0


def song_exist(song, edit=False):
    query, session = __ADAPTER.get_query(Song)

    query = query.filter(Song.title == song.title)

    if song.artist:
        query = query.filter(
            Artist.first_name == song.artist.first_name,
            Artist.last_name == song.artist.last_name,
        )

    if edit:
        query = query.filter(Song.id != song.id)

    songs = query.all()

    return len(songs) != 0


def artist_has_song(artist):
    query, session = __ADAPTER.get_query(Song)

    query = query.join(Artist).filter(Artist.id == artist.id)

    songs = query.all()

    return len(songs) != 0


def insert_song(song):
    if not song.title or not song.body or not song.artist:
        raise SongError('title, artist and body of song are required')

    song.title = song.title.capitalize()
    song.body = song.body.upper()

    if song_exist(song):
        raise SongError('song already exist')

    query, session = __ADAPTER.get_query(Song)

    session.merge(song.artist, load=False)
    session.add(song)
    session.commit()

    return True


def edit_song(song):
    if not song.title or not song.body or not song.artist:
        raise SongError('title, artist and body of song are required')

    song_to_edit, session = __ADAPTER.get(Song, song.id)

    song_to_edit.title = song.title.capitalize()
    song_to_edit.body = song.body.upper()

    if song_exist(song, True):
        raise SongError('song already exist')

    session.commit()

    return True


def delete_song(song):
    song, session = __ADAPTER.get(Song, song.id)

    session.delete(song)
    session.commit()

    return True


def insert_artist(artist):
    if not artist.first_name:
        raise SongError('first name of artist are required')

    artist.first_name = artist.first_name.capitalize()

    if artist.last_name:
        artist.last_name = artist.last_name.capitalize()

    if artist_exist(artist):
        raise SongError('artist already exist')

    query, session = __ADAPTER.get_query(Artist)

    session.add(artist)
    session.commit()

    return True


def edit_artist(artist):
    if not artist.first_name:
        raise SongError('first name of artist are required')

    artist_to_edit, session = __ADAPTER.get(Artist, artist.id)

    artist_to_edit.first_name = artist.first_name.capitalize()

    if artist.last_name:
        artist_to_edit.last_name = artist.last_name.capitalize()

    if artist_exist(artist, True):
        raise SongError('artist already exist')

    session.commit()

    return True

def delete_artist(artist):
    artist, session = __ADAPTER.get(Artist, artist.id)

    if artist_has_song(artist):
        raise SongError('cant delete artist, has songs associated')

    session.delete(artist)
    session.commit()

    return True

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
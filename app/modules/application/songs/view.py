# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from sqlalchemy import Column, Integer, String, Text, ForeignKey, func
from sqlalchemy.orm import relationship

import app.lib.orm as orm
import app.resources.modules.karaoke.options as ui_opts_resource
import app.resources.modules.karaoke.management as ui_manage_resource
import app.modules.utils as utils
from app.lib.helpers import get_projections_font, set_alignment, to_unicode

DELIMITER = '\n\n'
LINE_DELIMITER = '\n'


def configure_options(**kwargs):
    options = KaraokeOptions(kwargs['controls'].module_options_panel)
    options.set_dependents(kwargs)
    options.configure()

    return options


class SongError(Exception):
    pass


class KaraokeOptions(utils.ApplicationDBModule, utils.Slideable, utils.Searchable):
    __controls = {
        'add_song': {'cmdAddSong': 'clicked()'},
        'delete_song': {'cmdDeleteSong': 'clicked()'},
        'edit_song': {'cmdEditSong': 'clicked()'},
        'song_selected': {'lstSongs': 'itemClicked (QTableWidgetItem*)'},
        'show_song': {'lstSongs': 'itemDoubleClicked (QTableWidgetItem*)'}
    }

    def __init__(self, parent):
        utils.ApplicationDBModule.__init__(self, parent, None, ui_opts_resource.Ui_options(), self.__controls)

    def config_components(self):

        #Table configuration
        self._widget.lstSongs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._widget.lstSongs.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self._widget.lstSongs.clear()
        self._widget.lstSongs.hideColumn(0)
        self._widget.lstSongs.hideColumn(1)
        self._widget.lstSongs.hideColumn(2)

        self.callback('add_song', self.__add_song)
        self.callback('delete_song', self.__delete_song)
        self.callback('edit_song', self.__edit_song)
        self.callback('song_selected', self.__song_selected)
        self.callback('show_song', self.__show_song)

    def configure(self):

        self._controls.search_in_history(True)
        self._controls.add_module_options(self)
        self._controls.configure_search_box(self)

        self._statusbar.set_status('Song module loaded successfully')


    def keyPressEvent(self, e):

        if e.key() in [Qt.Key_Enter, Qt.Key_Return]:
            item = self._widget.lstSongs.currentItem()

            if item:
                self.__show_song(item)

        self._controls.keyPressEvent(e)
        self._toolbox.keyPressEvent(e)

    def __set_table_data(self, songs):

        def __set_row(*cells):
            row = self._widget.lstSongs.rowCount()
            self._widget.lstSongs.insertRow(row)

            for cell in cells:
                self._widget.lstSongs.setItem(row, cell.column, cell)

        self._widget.lstSongs.setRowCount(0)
        if songs:
            for song in songs:
                __set_row(
                    TableRow(0, str(song.id)),
                    TableRow(1, song.title),
                    TableRow(2, song.artist.fullName))

            self._widget.lstSongs.showColumn(1)
            self._widget.lstSongs.showColumn(2)

            self._widget.lstSongs.resizeColumnsToContents()
            self._widget.lstSongs.setFocus()
            self._widget.lstSongs.setCurrentCell(0, 0)
            self.__song_selected(self._widget.lstSongs.item(0, 0))

        else:
            self._widget.lstSongs.hideColumn(1)
            self._widget.lstSongs.hideColumn(2)

    def search(self, text=None):
        unicode_search_text = to_unicode(self._controls.search_box_text)

        songs = self.__songs_db(unicode_search_text)
        if songs:
            self._controls.append_to_history(unicode_search_text)
            self.__set_table_data(songs)
        else:
            self._statusbar.set_status('Song not found', True, 4)

        self._controls.search_text

    def __add_song(self):
        songManagement = SongManagement(self, 'Add Song')
        songManagement.show()

    def __edit_song(self):
        idItem = self._widget.lstSongs.item(self._widget.lstSongs.currentItem().row(), 0)

        songManagement = SongManagement(self, 'Edit Song', self.__song_db(int(idItem.text())))
        songManagement.show()

    def __delete_song(self):
        idItem = self._widget.lstSongs.item(self._widget.lstSongs.currentItem().row(), 0)

        self.__delete_song_db(int(idItem.text()))
        self._widget.lstSongs.removeRow(self._widget.lstSongs.currentItem().row())

        self._widget.cmdEditSong.setEnabled(False)
        self._widget.cmdDeleteSong.setEnabled(False)

    def __song_selected(self, item):

        self._widget.cmdEditSong.setEnabled(True)
        self._widget.cmdDeleteSong.setEnabled(True)

    def process_slides(self, preview_text, **kwargs):
        template, variables = self.template('song')
        splitted = preview_text.split(DELIMITER)
        slides = []

        image = '{0}/{1}/{2}'.format(
            self.config.get('GENERAL', 'images_dirs'),
            self.config.get('LIVE', 'backgrounds_dir'),
            self.config.get('SONG', 'background_image')
        )

        variables['image'] = image
        variables['slide_info'] = kwargs['title_and_artist']

        for slide in splitted:
            variables['lines'] = slide.split(LINE_DELIMITER)
            slides.append(template.render(variables))

        self._controls.set_slides()
        self._set_projection_item(slides)

    def __show_song(self, item):
        idItem = self._widget.lstSongs.item(item.row(), 0)

        song = self.__song_db(int(idItem.text()))
        self._previewer.set_text(song.body)

        self.process_slides(song.body, title_and_artist=song.titleAndArtist)

        if self._toolbox.direct_live:
            self._toolbox.go_to_live()

    def __songs_db(self, unicode_criteria):
        query, session = self._DBAdapter.get_query(Song)

        query = query.join(Song.artist).filter(
            (Artist.first_name.like('%{0}%'.format(unicode_criteria)))
            | (Artist.last_name.like('%{0}%'.format(unicode_criteria)))
            | (Song.title.like('%{0}%'.format(unicode_criteria)))
            | (Song.body.like('%{0}%'.format(unicode_criteria))))

        return query.all()

    def __song_db(self, idSong):
        query, session = self._DBAdapter.get_query(Song)

        song = query.filter(Song.id == idSong).one()
        session.merge(song.artist, load=True)
        session.close()

        return song

    def __delete_song_db(self, idSong):
        query, session = self._DBAdapter.get_query(Song)

        song = query.filter(Song.id == idSong).one()

        session.delete(song)
        session.commit()
        session.close()

        return True


class SongManagement(QtGui.QWizard, utils.ApplicationDBModule):
    __controls = {
        'search_artist': {'txtSearchArtist': 'returnPressed()'},
        'search_artist_button': {'cmdSearchArtist': 'clicked()'},
        'add_artist': {'cmdAddArtist': 'clicked()'},
        'edit_artist': {'cmdEditArtist': 'clicked()'},
        'delete_artist': {'cmdDeleteArtist': 'clicked()'},
        'artist_selected': {'lstArtists': 'itemClicked (QTableWidgetItem*)'}
    }

    def __init__(self, parent, title, song=None):
        self.__windowTitle = title
        self.__song = song
        utils.ApplicationDBModule.__init__(self, parent, QtGui.QWizard, ui_manage_resource.Ui_songManagement(),
                                           self.__controls)

    def instance_variable(self):
        utils.ApplicationDBModule.instance_variable(self)

        self.__txtSongBody = SongBody(self)
        self.songBodyPage = utils.ProjectionWizardPage(self, 'Song Body')

    def config_components(self):
        self.setWindowTitle(self.__windowTitle)
        self._widget.lblStatus.setVisible(False)
        self.button(QtGui.QWizard.FinishButton).clicked.connect(self.__save_song)
        self.setButtonText(QtGui.QWizard.FinishButton, 'Save')

        setattr(self._widget.lblArtistName, 'idArtist', None)

        #Configure Artist table
        self._widget.lstArtists.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self._widget.lstArtists.clear()
        self._widget.lstArtists.hideColumn(0)
        self._widget.lstArtists.hideColumn(1)

        #Callbacks
        self.callback('search_artist', self.__search_artist)
        self.callback('search_artist_button', self.__search_artist)
        self.callback('artist_selected', self.__artist_selected)
        self.callback('add_artist', self.__add_artist)
        self.callback('edit_artist', self.__edit_artist)
        self.callback('delete_artist', self.__delete_artist)


        #Song Configure
        if self.__song:
            self.setWindowTitle('{0} - ({1})'.format(self.__windowTitle, self.__song.titleAndArtist))

            self._widget.txtTitle.setText(self.__song.title)
            self.__txtSongBody.setText(self.__song.body)
            self._widget.lblArtistName.setText(self.__song.artist.fullName)
            self._widget.lblArtistName.idArtist = self.__song.artist.id

        font = get_projections_font(dict(self.config.items('FONT_PREVIEW')),self.config.getint('LIVE', 'DEFAULT_FONT_SIZE'))
        font.setPointSize(self.config.getint('SONG', 'MANAGEMENT_FONT_SIZE'))
        self.__txtSongBody.setFont(font)

        set_alignment(self.__txtSongBody, Qt.AlignCenter)
        self.__txtSongBody.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.__txtSongBody.setAcceptRichText(False)

        self.songBodyPage.add_widget(self.__txtSongBody)
        self.songBodyPage.callback('validate', self.__validate_song)
        self.setPage(2, self.songBodyPage)

        self.set_status('Ready')

    def set_status(self, status, error=False):
        self._widget.lblStatus.setText(status.capitalize())
        self._widget.lblStatus.setVisible(True)

    def __set_table_row(self, *cells):
        row = self._widget.lstArtists.rowCount()
        self._widget.lstArtists.insertRow(row)

        for cell in cells:
            self._widget.lstArtists.setItem(row, cell.column, cell)

    def __set_table_data(self, artists):

        self._widget.lstArtists.setRowCount(0)
        if artists:
            for artist in artists:
                self.__set_table_row(
                    TableRow(0, str(artist.id)),
                    TableRow(1, artist.fullName))

            self._widget.lstArtists.showColumn(1)

        else:
            self._widget.lstArtists.hideColumn(1)

    def __search_artist(self):
        search_text = self._widget.txtSearchArtist.text()

        artists = self.__artists_db(search_text)
        self.__set_table_data(artists)

        self._widget.txtSearchArtist.setText('')
        self.set_status('Ready')

    def __artist_selected(self, item):

        idItem = self._widget.lstArtists.item(item.row(), 0)
        artistNameItem = self._widget.lstArtists.item(item.row(), 1)

        self._widget.lblArtistName.idArtist = int(idItem.text())
        self._widget.lblArtistName.setText(artistNameItem.text())

        self._widget.cmdEditArtist.setEnabled(True)
        self._widget.cmdDeleteArtist.setEnabled(True)

    def __add_artist(self):
        text, accept = QtGui.QInputDialog.getText(QtGui.QInputDialog(), 'Add Artist', 'Artist', QtGui.QLineEdit.Normal)

        if accept and text:
            values = text.split(',')
            artist = Artist()

            artist.first_name = str(values[0])
            try:
                artist.last_name = str(values[1])
            except IndexError:
                pass

            try:
                self.__add_artist_db(artist)
                self.__set_table_row(
                    TableRow(0, str(artist.id)),
                    TableRow(1, artist.fullName))

                self._widget.lstArtists.setFocus()
                self.__artist_selected(self._widget.lstArtists.item(self._widget.lstArtists.rowCount() - 1, 0))
                self.set_status('Ready')
            except SongError, e:
                self.set_status(e.message, True)

    def __edit_artist(self):

        idItem = self._widget.lstArtists.item(self._widget.lstArtists.currentRow(), 0)
        nameItem = self._widget.lstArtists.item(self._widget.lstArtists.currentRow(), 1)

        artist = self.__artist_db(int(idItem.text()))

        text, accept = QtGui.QInputDialog.getText(QtGui.QInputDialog(), 'Edit Artist', 'Artist',
                                                  QtGui.QLineEdit.Normal,
                                                  '{0},{1}'.format(artist.first_name, artist.last_name))

        if accept and text:
            values = text.split(',')

            artist.first_name = str(values[0])
            try:
                artist.last_name = str(values[1])
            except IndexError:
                pass

            try:
                self.__edit_artist_db(artist)

                nameItem.setText(artist.fullName)
                self._widget.lblArtistName.setText(artist.fullName)

                self.set_status('Ready')
            except SongError, e:
                self.set_status(e.message, True)

    def __delete_artist(self):
        idItem = self._widget.lstArtists.item(self._widget.lstArtists.currentItem().row(), 0)

        try:
            self.__delete_artist_db(int(idItem.text()))
            self._widget.lstArtists.removeRow(self._widget.lstArtists.currentItem().row())

            self._widget.lblArtistName.idArtist = None
            self._widget.lblArtistName.setText('')

            self._widget.cmdEditArtist.setEnabled(False)
            self._widget.cmdDeleteArtist.setEnabled(False)

            self.set_status('Ready')
        except SongError, e:
            self.set_status(e.message, True)

    def __validate_song(self):

        song = Song() if not self.__song else self.__song

        if not self._widget.txtTitle.text() or not self.__txtSongBody.toPlainText() or not self._widget.lblArtistName.text():
            self.set_status('Song cannot be add [title, artist and body of song are required]')
            self.back()
            return False

        song.title = unicode(self._widget.txtTitle.text(), 'latin')
        song.artist = self.__artist_db(int(self._widget.lblArtistName.idArtist))
        song.body = unicode(self.__txtSongBody.toPlainText(), 'latin')

        exist = self.__exist_song_db(song, self.__song)

        if exist:
            self.set_status('Song cannot be add [song already exist]')
            self.back()

        return not exist

    def __save_song(self):

        song = Song() if not self.__song else self.__song

        song.title = unicode(self._widget.txtTitle.text(), 'latin')
        song.artist = self.__artist_db(int(self._widget.lblArtistName.idArtist))
        song.body = unicode(self.__txtSongBody.toPlainText(), 'latin')

        try:
            self.__save_song_db(song, self.__song)
        except SongError:
            pass


    def __artists_db(self, criteria):
        query, session = self._DBAdapter.get_query(Artist)

        query = query.filter(
            (Artist.first_name.like('%{0}%'.format(criteria)))
            | (Artist.last_name.like('%{0}%'.format(criteria))))

        artists = query.all()
        session.close()

        return artists

    def __artist_db(self, idArtist):
        query, session = self._DBAdapter.get_query(Artist)

        artist = query.filter(Artist.id == idArtist).one()
        session.close()

        return artist


    def __add_artist_db(self, artist):
        if not artist.first_name:
            raise SongError('Artist cannot be add [first name of artist is required]')

        artist.first_name = artist.first_name.strip().capitalize()

        if artist.last_name:
            artist.last_name = artist.last_name.strip().capitalize()

        if self.__exist_artist_db(artist):
            raise SongError('Artist cannot be add [artist already exist]')

        query, session = self._DBAdapter.get_query(Artist)

        session.add(artist)
        session.commit()
        session.refresh(artist)
        session.close()

        return True

    def __edit_artist_db(self, artist):
        if not artist.first_name:
            raise SongError('Artist cannot be edit [first name of artist is required]')

        artist_to_edit, session = self._DBAdapter.get(Artist, artist.id)

        artist_to_edit.first_name = artist.first_name.strip().capitalize()

        if artist.last_name:
            artist_to_edit.last_name = artist.last_name.strip().capitalize()

        if self.__exist_artist_db(artist, True):
            raise SongError('Artist cannot be edit [artist already exist]')

        session.commit()
        session.close()

        return True


    def __delete_artist_db(self, idArtist):
        query, session = self._DBAdapter.get_query(Artist)

        artist = query.filter(Artist.id == idArtist).one()

        if not self.__artist_has_song(artist):
            session.delete(artist)
            session.commit()
            session.close()

            return True
        else:
            raise SongError('Artist cannot be delete [has songs]')

    def __artist_has_song(self, artist):
        query, session = self._DBAdapter.get_query(Song)

        query = query.join(Artist).filter(Artist.id == artist.id)

        songs = query.all()
        session.close()

        return len(songs) != 0

    def __exist_artist_db(self, artist, edit=False):
        query, session = self._DBAdapter.get_query(Artist)

        query = query.filter(Artist.first_name == artist.first_name)

        if artist.last_name:
            query = query.filter(Artist.last_name == artist.last_name)

        if edit:
            query = query.filter(Artist.id != artist.id)

        artists = query.all()
        session.close()

        return len(artists) != 0

    def __save_song_db(self, song, edit=False):
        if not song.title or not song.body or not song.artist:
            raise SongError('Song cannot be add [title, artist and body of song are required]')

        song.title = song.title.strip().capitalize()
        song.body = song.body.strip().upper()

        if self.__exist_song_db(song, edit):
            raise SongError('Song cannot be add [song already exist]')

        query, session = self._DBAdapter.get_query(Song)

        if edit:
            session.merge(song)
        else:
            session.add(song)

        session.commit()
        session.close()

        return True

    def __exist_song_db(self, song, edit=False):
        query, session = self._DBAdapter.get_query(Song)

        query = query.filter(func.lower(Song.title) == song.title.lower())

        if song.artist:
            if song.artist.first_name:
                query = query.filter(func.lower(Artist.first_name) == song.artist.first_name.lower())

            if song.artist.last_name:
                query = query.filter(func.lower(Artist.last_name) == song.artist.last_name.lower())

        if edit:
            query = query.filter(Song.id != song.id)

        songs = query.all()
        session.close()

        return len(songs) != 0


class SongBody(QtGui.QTextEdit):
    def __init__(self, parent):
        super(SongBody, self).__init__(parent)

    def keyPressEvent(self, event):
        super(SongBody, self).keyPressEvent(event)

        if event.matches(QtGui.QKeySequence.Paste):
            set_alignment(self, Qt.AlignCenter)


class TableRow(QtGui.QTableWidgetItem):
    def __init__(self, column, songPropertyValue):
        QtGui.QTableWidgetItem.__init__(self, songPropertyValue)

        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.column = column

    def __repr__(self):
        return u'<%s>' % self.text()


class Artist(orm.BaseTable):
    __tablename__ = 'Artist'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    songs = relationship("Song", backref="Artist")

    @property
    def fullName(self):
        return self.first_name + ' ' + self.last_name if self.last_name else self.first_name

    def __repr__(self):
        return '<{0} - {1}>'.format(self.id, self.fullName)


class Song(orm.BaseTable):
    __tablename__ = 'Song'

    id = Column(Integer, primary_key=True)
    __id_artist = Column('id_artist', Integer, ForeignKey('Artist.id'))
    artist = relationship('Artist')
    title = Column(String(100))
    body = Column(Text)

    @property
    def titleAndArtist(self):
        return u'{title} - {artist}'.format(title=self.title.encode('latin'), artist=self.artist.fullName)

    def __repr__(self):
        return self.titleAndArtist

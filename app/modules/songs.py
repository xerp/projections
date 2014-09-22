__author__ = 'santiago.depedro'

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
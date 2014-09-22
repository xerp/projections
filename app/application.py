# -*- coding: utf-8 -*-
import time
import threading
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from functools import partial

from modules import bible, songs
from resources import resources, song_manage
from helpers import get_projections_font, get_images_view, set_alignment, ProjectionError, ImagesViewModel
from helpers import get_songs_completer, artists_model,remove_pycs
from components import SongBody
from ConfigParser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')


def main():
    app = QtGui.QApplication(sys.argv)
    frame = Principal()
    frame.show()
    remove_pycs()
    sys.exit(app.exec_())


class Principal(QtGui.QFrame):
    in_live = False
    direct_live = False
    default_frame_size = None

    slides = []
    slide_length = len(slides)
    slide_position = 0
    selected_song = None

    def __init__(self):
        QtGui.QFrame.__init__(self)
        self.__window = resources.Ui_frmPrincipal()
        self.__window.setupUi(self)

        self.full_screen = FullScreenWindow(self)

        self.set_handlers()
        self.window_config()

    def window_config(self):

        self.setWindowTitle("{0} Manager (beta)".format(conf.get('GENERAL', 'TITLE')))

        self.__window.txtPreview.setFont(get_projections_font(dict(conf.items('FONT_PREVIEW'))))

        self.__window.cmdColorScreen.setText('{0} (F9)'.format(conf.get('LIVE', 'DEFAULT_COLOR').upper()))
        self.__window.cmdColorScreen.setShortcut("F9")

        self.__window.txtSearch.setPlaceholderText("Search in bible (F3)")

        self.__window.sLiveFont.setValue(
            int(dict(conf.items('FONT_LIVE')).get('size', conf.getint('LIVE', 'DEFAULT_FONT_SIZE'))))

        self.set_in_live(False)

        self.set_status('Ready')

        app = QtGui.QApplication.instance()
        screens = app.desktop().numScreens()

        self.__window.cbLiveIn.addItems(map(lambda s: 'Screen {0}'.format(s), range(1, screens + 1)))

        if screens >= conf.getint('LIVE', 'DEFAULT_SCREEN'):
            self.__window.cbLiveIn.setCurrentIndex(conf.getint('LIVE', 'DEFAULT_SCREEN') - 1)

        self.default_frame_size = self.size()

        try:
            images = get_images_view()
            model = ImagesViewModel(images, self.__window.cbImagesView)
            self.__window.cbImagesView.setModel(model)

            try:
                self.__window.cbImagesView.setCurrentIndex(images.index(conf.get('GENERAL', 'DEFAULT_IMAGE')))
            except Exception:
                pass

        except Exception, e:
            self.set_status(str(e), True)

    def set_handlers(self):

        QtCore.QObject.connect(self.__window.txtSearch, QtCore.SIGNAL('returnPressed()'), self.txtSearch_enter_pressed)
        QtCore.QObject.connect(self.__window.cmdLive, QtCore.SIGNAL('toggled(bool)'), self.set_in_live)
        QtCore.QObject.connect(self.__window.cmdFullScreen, QtCore.SIGNAL('toggled(bool)'), self.cmdFullScreen_toggled)
        QtCore.QObject.connect(self.__window.cmdMainView, QtCore.SIGNAL('clicked()'), self.cmdMainView_clicked)
        QtCore.QObject.connect(self.__window.cmdColorScreen, QtCore.SIGNAL('clicked()'), self.cmdColorScreen_clicked)
        QtCore.QObject.connect(self.__window.cmdPrevious, QtCore.SIGNAL('clicked()'), self.cmdPrevious_clicked)
        QtCore.QObject.connect(self.__window.cmdNext, QtCore.SIGNAL('clicked()'), self.cmdNext_clicked)
        QtCore.QObject.connect(self.__window.sLiveFont, QtCore.SIGNAL('sliderMoved(int)'), self.sLiveFont_valueChanged)
        QtCore.QObject.connect(self.__window.sLiveFont, QtCore.SIGNAL('valueChanged(int)'), self.sLiveFont_valueChanged)
        QtCore.QObject.connect(self.__window.rbBible, QtCore.SIGNAL('clicked()'), self.rbBible_clicked)
        QtCore.QObject.connect(self.__window.rbSong, QtCore.SIGNAL('clicked()'), self.rbSong_clicked)
        QtCore.QObject.connect(self.__window.cmdAddSong, QtCore.SIGNAL('clicked()'), self.cmdAddSong_clicked)
        QtCore.QObject.connect(self.__window.cmdEditSong, QtCore.SIGNAL('clicked()'), self.cmdEditSong_clicked)
        QtCore.QObject.connect(self.__window.cmdDeleteSong, QtCore.SIGNAL('clicked()'), self.cmdDeleteSong_clicked)
        QtCore.QObject.connect(self.__window.cmdRefreshImageView, QtCore.SIGNAL('clicked()'),
                               self.cmdRefreshImageView_clicked)
        QtCore.QObject.connect(self.__window.cmdCompactView, QtCore.SIGNAL('toggled(bool)'),
                               self.cmdCompactView_toggled)

        QtCore.QObject.connect(self.__window.cmdDirectToLive, QtCore.SIGNAL('toggled(bool)'),
                               self.cmdDirectToLive_toggled)

        QtCore.QObject.connect(self.__window.cmdGotoLive, QtCore.SIGNAL('clicked()'),
                               self.cmdGotoLive_clicked)

    def set_status(self, msg, error=False, time_to_hide=None, msg_after_hide=''):
        pixmap = QtGui.QPixmap(":/main/icons/{0}.png".format("error-24" if error else "valid-24"))

        self.__window.lblGeneralStatus.setText(msg.capitalize())
        self.__window.lblStatusIcon.setVisible(True)
        self.__window.lblStatusIcon.setPixmap(pixmap)

        if time_to_hide:
            def worker():
                time.sleep(time_to_hide)
                self.__window.lblGeneralStatus.setText(msg_after_hide)
                self.__window.lblStatusIcon.setVisible(True if msg_after_hide else False)

            thread = threading.Thread(target=worker)
            thread.start()

    def set_in_live(self, in_live):

        self.in_live = in_live

        self.__window.cmdFullScreen.setChecked(False)
        self.__window.cmdDirectToLive.setChecked(False)

        self.__window.cmdDirectToLive.setEnabled(in_live)
        self.__window.cmdGotoLive.setEnabled(in_live)
        self.__window.cmdMainView.setEnabled(in_live)
        self.__window.cmdColorScreen.setEnabled(in_live)
        self.__window.cmdFullScreen.setEnabled(in_live)
        self.__window.cbLiveIn.setEnabled(not in_live)

        self.__window.lblButton.setText('')

        self.full_screen.set_visible(in_live, self.__window.cbLiveIn.currentIndex() + 1)
        self.__window.lblLive.setEnabled(in_live)
        self.__window.lblLive.setStyleSheet('color: rgb(255, 0, 0);' if in_live else '')

        if in_live:
            self.full_screen.set_color(Qt.red)

        else:
            self.__window.cmdPrevious.setEnabled(False)
            self.__window.cmdNext.setEnabled(False)
            self.__window.cmdLive.setChecked(False)

        self.set_status('In live' if in_live else 'Off live')

        self.set_seeker()

    def set_buttons_slides(self, max_slides):
        self.remove_buttons_slides()

        cols = 5
        for slide in range(1, max_slides + 1):
            button = QtGui.QPushButton(str(slide))

            button.setMaximumSize(QtCore.QSize(30, 30))
            button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

            button.clicked.connect(partial(self.onBtnSlide_clicked, slide))

            items = self.__window.cmdSlides.count()
            row = items / cols
            col = items % cols

            self.__window.cmdSlides.addWidget(button, row, col)

    def remove_buttons_slides(self):

        for index in range(0, self.__window.cmdSlides.count() + 1):
            row, col, rspan, cspan = self.__window.cmdSlides.getItemPosition(index)
            item = self.__window.cmdSlides.itemAtPosition(row, col)

            if item:
                item.widget().deleteLater()

    def set_slides(self, whole_text, delimiter, limit=conf.getint('BIBLE', 'FORWARD_LIMIT')):

        if self.__window.chkSearchForward.isChecked():
            splitted = whole_text.split(delimiter)[:limit]
        else:
            splitted = whole_text.split(delimiter)

        self.slides = filter(lambda s: s and s != '(END)', splitted)
        self.slide_length = len(self.slides)
        self.slide_position = 0

        self.set_seeker()

    def set_seeker(self):
        self.remove_buttons_slides()

        if self.in_live and self.slide_length > 1:
            self.set_buttons_slides(self.slide_length)

            self.__window.cmdPrevious.setEnabled(False)
            self.__window.cmdNext.setEnabled(True)

    def cmdAddSong_clicked(self):

        try:
            a_song = SongManagement(self, 'Add Song')
            a_song.exec_()

            completer = get_songs_completer(self.__window.txtSearch)
            self.__window.txtSearch.setCompleter(completer)
            self.__window.txtSearch.setFocus()

            self.set_status('Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

        except songs.SongError, e:
            self.set_status(str(e), True)

    def cmdEditSong_clicked(self):
        try:
            a_song = SongManagement(self, 'Edit Song')
            a_song.set_song(self.selected_song)
            a_song.exec_()

            self.__window.txtPreview.clear()
            self.__window.txtSearch.clear()

            completer = get_songs_completer(self.__window.txtSearch)
            self.__window.txtSearch.setCompleter(completer)
            self.__window.txtSearch.setFocus()

            self.__window.cmdEditSong.setEnabled(False)
            self.__window.cmdDeleteSong.setEnabled(False)

            self.selected_song = None

            self.set_status('Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

        except songs.SongError, e:
            self.set_status(str(e), True)


    def cmdDeleteSong_clicked(self):

        self.selected_song = self.__window.txtSearch.completer().model().selected()
        songs.delete_song(self.selected_song)
        self.selected_song = None

        self.__window.txtPreview.clear()
        self.__window.txtSearch.clear()

        completer = get_songs_completer(self.__window.txtSearch)
        self.__window.txtSearch.setCompleter(completer)
        self.__window.txtSearch.setFocus()

        self.__window.cmdEditSong.setEnabled(False)
        self.__window.cmdDeleteSong.setEnabled(False)

        self.set_status('Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

    def txtSearch_enter_pressed(self):
        text = self.__window.txtSearch.text()
        result = ''
        delimiter = ''

        self.set_status('Ready')

        if self.__window.rbBible.isChecked():
            if self.__window.chkSearchForward.isChecked():
                text = '{0}-'.format(text)

            delimiter = bible.DELIMITER
            try:
                result = bible.search_verse(text)
            except bible.BibleError, e:
                self.set_status(str(e), True)

        else:
            delimiter = songs.DELIMITER

            try:
                self.selected_song = self.__window.txtSearch.completer().model().selected()
                result = self.selected_song.body

                self.__window.cmdEditSong.setEnabled(True)
                self.__window.cmdDeleteSong.setEnabled(True)
            except songs.SongError, e:
                self.set_status(str(e), True)

        self.set_slides(result, delimiter)

        self.__window.txtPreview.setText(result)

        if self.direct_live:
            self.full_screen.set_text(self.slides[self.slide_position],
                                      self.__window.sLiveFont.value())

    def cmdRefreshImageView_clicked(self):

        model = ImagesViewModel(get_images_view(), self.__window.cbImagesView)
        self.__window.cbImagesView.setModel(model)

    def rbBible_clicked(self):
        self.__window.txtSearch.setPlaceholderText('Search in bible (F3)')
        self.__window.txtSearch.setCompleter(None)

        self.__window.txtSearch.selectAll()
        self.__window.txtSearch.setFocus()

        self.__window.cmdEditSong.setEnabled(False)
        self.__window.cmdDeleteSong.setEnabled(False)
        self.selected_song = None

        self.set_status('Bible search')

    def rbSong_clicked(self):
        self.__window.txtSearch.setPlaceholderText('Search a song (F3)')

        try:
            completer = get_songs_completer(self.__window.txtSearch)
            self.__window.txtSearch.setCompleter(completer)

            self.set_status(
                'Songs loaded successfully [ count: {0} ]'.format(completer.completionModel().rowCount()))

        except songs.SongError:
            self.set_status('One error occurred try loading songs', True)

        self.__window.txtSearch.selectAll()
        self.__window.txtSearch.setFocus()

    def cmdFullScreen_toggled(self, active):
        self.full_screen.set_full_screen(active)

        self.__window.lblFullScreen.setEnabled(active)
        self.__window.lblFullScreen.setStyleSheet('color: rgb(0, 0, 255);' if active else '')

    def cmdMainView_clicked(self):
        try:

            self.full_screen.set_image(self.__window.cbImagesView.model().selected())

            self.__window.lblButton.setText('Main View')
            self.set_status('Live in Main View')
        except ProjectionError, e:
            self.set_status(str(e), True)

    def cmdColorScreen_clicked(self):
        self.full_screen.set_color()

        self.__window.lblButton.setText(conf.get('LIVE', 'DEFAULT_COLOR').upper())
        self.set_status('Live in Black')

    def cmdDirectToLive_toggled(self, active):
        self.direct_live = active
        self.set_status('Direct live {0}'.format('on' if active else 'off'))

    def cmdGotoLive_clicked(self):
        text = self.__window.txtPreview.toPlainText()

        if text:
            self.full_screen.set_text(self.slides[self.slide_position],
                                      self.__window.sLiveFont.value())

            if self.in_live:
                self.set_seeker()

        self.set_status('View refreshed')

    def cmdPrevious_clicked(self):

        self.slide_position -= 1
        self.full_screen.set_text(self.slides[self.slide_position],
                                  self.__window.sLiveFont.value())

        self.__window.cmdNext.setEnabled(True)
        self.__window.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

    def cmdNext_clicked(self):

        self.slide_position += 1
        self.full_screen.set_text(self.slides[self.slide_position],
                                  self.__window.sLiveFont.value())

        self.__window.cmdPrevious.setEnabled(True)
        self.__window.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)

    def onBtnSlide_clicked(self, button_num):

        self.slide_position = button_num - 1
        self.full_screen.set_text(self.slides[self.slide_position],
                                  self.__window.sLiveFont.value())

        self.__window.sLiveFont.setValue(
            int(dict(conf.items('FONT_LIVE')).get('size', conf.get('LIVE', 'DEFAULT_FONT_SIZE'))))

        self.__window.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)
        self.__window.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

    def cmdCompactView_toggled(self, active):
        n_active = not active

        self.__window.dockProjectionsTools.setVisible(n_active)
        self.__window.txtPreview.setVisible(n_active)

        if active:
            self.__window.dockProjectionsControls.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
            self.resize(self.__window.dockProjectionsControls.minimumWidth(), self.default_frame_size.height())
            self.setWindowFlags(Qt.WindowTitleHint and Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.__window.dockProjectionsControls.setFeatures(
                QtGui.QDockWidget.DockWidgetFloatable or QtGui.QDockWidget.DockWidgetMovable)
            self.resize(self.default_frame_size)
            self.setWindowFlags(Qt.WindowShadeButtonHint)
            self.show()

        self.set_status('Compact view {0}'.format('on' if active else 'off'))

    def sLiveFont_valueChanged(self, value):

        if self.in_live:
            try:
                self.full_screen.set_text(self.slides[self.slide_position], value)
            except IndexError:
                pass

        self.set_status('Font size: {0} point(s)'.format(value), time_to_hide=2)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_F3:
            self.__window.txtSearch.selectAll()
            self.__window.txtSearch.setFocus()

    def closeEvent(self, e):
        self.full_screen.set_visible(False)
        self.full_screen.hide()


class FullScreenWindow(QtGui.QFrame):
    size = QtCore.QSize(400, 400)
    screen_geometry = None

    def __init__(self, parent):
        QtGui.QFrame.__init__(self)
        self.parent = parent

        self.init_objects()
        self.init_component()

    def init_objects(self):
        self.main_layout = QtGui.QGridLayout(self)
        self.image = QtGui.QLabel()
        self.lblLive = QtGui.QTextEdit(self)

    def init_component(self):
        self.setWindowTitle('{0} Live Window (beta)'.format(conf.get('GENERAL', 'TITLE')))
        self.setWindowFlags(Qt.CustomizeWindowHint or Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.lblLive.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)

        self.lblLive.setReadOnly(True)
        self.lblLive.setVisible(True)

        self.main_layout.addWidget(self.lblLive)

        self.image.setScaledContents(False)

        self.reset()

    def closeEvent(self, e):
        self.parent.set_in_live(False)

    def set_visible(self, visible, screen=1):
        app = QtGui.QApplication.instance()

        self.screen_geometry = app.desktop().screenGeometry(screen)

        geometry = self.geometry()
        geometry.setX(self.screen_geometry.x())
        geometry.setY(self.screen_geometry.y())
        self.setGeometry(geometry)

        self.reset()
        self.show() if visible else self.hide()

    def reset(self):
        self.set_full_screen(False)
        self.setFixedSize(self.size)

    def __add_child(self, child):
        child.setVisible(True)
        self.main_layout.addWidget(child)

    def __remove_children(self):
        widgets = ['image', 'lblLive']

        for widget in widgets:
            obj = getattr(self, widget)

            obj.setVisible(False)
            self.main_layout.removeWidget(obj)

    def set_full_screen(self, full_screen):
        try:
            self.setFixedSize(self.screen_geometry.size() if full_screen else self.size)
        except Exception:
            raise ProjectionError('window must be visible before full_screen')

    def set_color(self, color=QtGui.QColor(conf.get('LIVE', 'DEFAULT_COLOR'))):
        self.__remove_children()

        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def set_image(self, image_file):
        self.set_color()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        if not image_file:
            raise ProjectionError('error occurred trying to loading image')

        image = QtGui.QImage()
        image.load(image_file)

        if image.isNull():
            raise ProjectionError(
                'image view not found [ path:{image} ]'.format(image=image_file[:20]))

        image = image.scaled(self.screen_geometry.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.image.setPixmap(QtGui.QPixmap.fromImage(image))
        self.image.setAlignment(Qt.AlignCenter)

        self.__add_child(self.image)

    def set_text(self, text, font_size=None,
                 text_color=conf.get('LIVE', 'DEFAULT_TEXT_COLOR'),
                 background_color=conf.get('LIVE', 'DEFAULT_BACKGROUND_COLOR'),
                 justification=Qt.AlignCenter):
        self.set_color()

        palette = self.lblLive.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(background_color))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(text_color))
        self.lblLive.setPalette(palette)

        text_live_margin = dict(conf.items('TEXT_LIVE_MARGIN'))
        self.main_layout.setContentsMargins(float(text_live_margin['left']), float(text_live_margin['top']),
                                            float(text_live_margin['right']), float(text_live_margin['bottom']))

        font = get_projections_font(dict(conf.items('FONT_LIVE')))

        if font_size:
            font.setPointSize(font_size)

        self.lblLive.setCurrentFont(font)
        self.lblLive.setText(text)

        set_alignment(self.lblLive, justification)

        self.__add_child(self.lblLive)

        if self.lblLive.verticalScrollBar().isVisible():
            self.set_text(text, font_size - 2, text_color, background_color, justification)


class SongManagement(QtGui.QDialog):
    SONG_ADD_MODE = 0
    SONG_EDIT_MODE = 1
    __edited_artist = None
    __song = None

    def __init__(self, parent, title, mode=SONG_ADD_MODE):
        QtGui.QDialog.__init__(self, parent, Qt.Tool)
        self.__window = song_manage.Ui_frmSongManagement()
        self.__window.setupUi(self)
        self.setWindowTitle(title)

        self.mode = mode
        self.set_handlers()
        self.window_config()

        self.set_status('Ready')

    def set_handlers(self):

        self.__window.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.cmdSave_clicked)
        self.__window.cmdAddArtist.clicked.connect(self.cmdAddArtist_clicked)
        self.__window.cmdEditArtist.clicked.connect(self.cmdEditArtist_clicked)
        self.__window.cmdDeleteArtist.clicked.connect(self.cmdDeleteArtist_clicked)

    def window_config(self):

        self.txtBody = SongBody(self)

        font = get_projections_font(dict(conf.items('FONT_LIVE')))
        font.setPointSize(conf.getint('SONG', 'MANAGEMENT_FONT_SIZE'))
        self.txtBody.setFont(font)

        set_alignment(self.txtBody, Qt.AlignCenter)
        self.txtBody.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtBody.setAcceptRichText(False)
        self.setTabOrder(self.__window.cbArtist, self.txtBody)
        self.__window.verticalLayout.insertWidget(1, self.txtBody)

        artists_model(self.__window.cbArtist)
        self.__window.txtTitle.setFocus()

    def set_status(self, status, error=False):
        self.__window.lblStatus.setText(status.capitalize())

    def set_song(self, song):

        if not song:
            raise songs.SongError('Non song selected')

        self.mode = self.SONG_EDIT_MODE
        self.__song = song

        self.__window.txtTitle.setText(song.title)
        self.txtBody.setText(song.body)
        set_alignment(self.txtBody, Qt.AlignCenter)

    def cmdSave_clicked(self):
        song = songs.Song() if self.mode == self.SONG_ADD_MODE else self.__song

        song.title = unicode(self.__window.txtTitle.text().toUtf8(), 'utf-8')
        song.body = unicode(self.txtBody.toPlainText().toUtf8(), 'utf-8')

        try:
            song.artist = self.__window.cbArtist.model().selected()
        except AssertionError:
            pass

        try:
            if self.mode == self.SONG_ADD_MODE:
                songs.insert_song(song)
            else:
                songs.edit_song(song)

            self.hide()
        except songs.SongError, e:
            self.set_status(str(e))

    def cmdAddArtist_clicked(self):

        text, accept = QtGui.QInputDialog.getText(QtGui.QInputDialog(), 'Add Artist', 'Artist', QtGui.QLineEdit.Normal)

        if accept and text:
            values = text.split(',')
            artist = songs.Artist()

            artist.first_name = str(values[0])
            try:
                artist.last_name = str(values[1])
            except IndexError:
                pass

            try:
                songs.insert_artist(artist)
                artists_model(self.__window.cbArtist)
            except songs.SongError, e:
                self.set_status(str(e), True)

    def cmdEditArtist_clicked(self):
        artist = self.__window.cbArtist.model().selected()

        text, accept = QtGui.QInputDialog.getText(QtGui.QInputDialog(), 'Edit Artist', 'Artist',
                                                  QtGui.QLineEdit.Normal,
                                                  '{0},{1}'.format(artist.first_name, artist.last_name))

        if accept and text:
            values = text.split(',')

            artist.first_name = str(values[0]).strip(' ')
            try:
                artist.last_name = str(values[1]).strip(' ')
            except IndexError:
                pass

            try:
                songs.edit_artist(artist)
                artists_model(self.__window.cbArtist)
            except songs.SongError, e:
                self.set_status(str(e), True)

    def cmdDeleteArtist_clicked(self):
        artist = self.__window.cbArtist.model().selected()

        try:
            songs.delete_artist(artist)
            artists_model(self.__window.cbArtist)
        except songs.SongError, e:
            self.set_status(str(e), True)



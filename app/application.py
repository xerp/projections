# -*- coding: utf-8 -*-
import time
import threading
import sys

from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
#from functools import partial

from modules.core import toolbox, statusbar, previewer, controls

#from modules import bible, songs
#from helpers import get_projections_font, get_images_view, set_alignment, ProjectionError, ImagesViewModel
#from helpers import get_songs_completer, artists_model,remove_pycs
#from components import SongBody

def main():
    app = QtGui.QApplication(sys.argv)
    frame = Application()
    frame.show()
    #remove_pycs()
    sys.exit(app.exec_())


class Application(QtGui.QFrame):
    default_frame_size = None
#     selected_song = None

    def __init__(self):
        QtGui.QFrame.__init__(self)

        self.config = ConfigParser()
        self.config.read('config.ini')

        self.configure_core_modules()
        self.window_config()


    def configure_core_modules(self):
        vBoxMainLayout = QtGui.QVBoxLayout()
        
        #ToolBox
        self.__toolbox = toolbox.ToolBox()
        vBoxMainLayout.addWidget(self.__toolbox)

        #Splitter
        splitter = QtGui.QSplitter(self)

        #Previewer
        self.__previewer = previewer.Previewer()
        splitter.addWidget(self.__previewer)

        #Controls
        self.__controls = controls.Controls()
        splitter.addWidget(self.__controls)
        self.__controls.set_images()

        splitter.setSizes([700,400])
        vBoxMainLayout.addWidget(splitter)
        
        #StatusBar
        self.__statusbar = statusbar.StatusBar()
        vBoxMainLayout.addWidget(self.__statusbar)
        
        self.setLayout(vBoxMainLayout)

    def window_config(self):

        self.setWindowTitle("{0} Manager (beta)".format(self.config.get('GENERAL', 'TITLE')))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/main/icons/video-projector.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.resize(900,600)


#         self.__window.txtPreview.setFont(get_projections_font(dict(conf.items('FONT_PREVIEW'))))


#         self.__window.txtSearch.setPlaceholderText("Search in bible (F3)")

#         self.__window.sLiveFont.setValue(
#             int(dict(conf.items('FONT_LIVE')).get('size', conf.getint('LIVE', 'DEFAULT_FONT_SIZE'))))

#         self.set_in_live(False)

#         self.set_status('Ready')

#         

#         self.default_frame_size = self.size()



#     def set_handlers(self):

#         QtCore.QObject.connect(self.__window.txtSearch, QtCore.SIGNAL('returnPressed()'), self.txtSearch_enter_pressed)
#         QtCore.QObject.connect(self.__window.cmdLive, QtCore.SIGNAL('toggled(bool)'), self.set_in_live)
#         QtCore.QObject.connect(self.__window.cmdFullScreen, QtCore.SIGNAL('toggled(bool)'), self.cmdFullScreen_toggled)
#         QtCore.QObject.connect(self.__window.cmdMainView, QtCore.SIGNAL('clicked()'), self.cmdMainView_clicked)
#         QtCore.QObject.connect(self.__window.cmdColorScreen, QtCore.SIGNAL('clicked()'), self.cmdColorScreen_clicked)
#         QtCore.QObject.connect(self.__window.cmdPrevious, QtCore.SIGNAL('clicked()'), self.cmdPrevious_clicked)
#         QtCore.QObject.connect(self.__window.cmdNext, QtCore.SIGNAL('clicked()'), self.cmdNext_clicked)
#         QtCore.QObject.connect(self.__window.sLiveFont, QtCore.SIGNAL('sliderMoved(int)'), self.sLiveFont_valueChanged)
#         QtCore.QObject.connect(self.__window.sLiveFont, QtCore.SIGNAL('valueChanged(int)'), self.sLiveFont_valueChanged)
#         QtCore.QObject.connect(self.__window.rbBible, QtCore.SIGNAL('clicked()'), self.rbBible_clicked)
#         QtCore.QObject.connect(self.__window.rbSong, QtCore.SIGNAL('clicked()'), self.rbSong_clicked)
#         QtCore.QObject.connect(self.__window.cmdAddSong, QtCore.SIGNAL('clicked()'), self.cmdAddSong_clicked)
#         QtCore.QObject.connect(self.__window.cmdEditSong, QtCore.SIGNAL('clicked()'), self.cmdEditSong_clicked)
#         QtCore.QObject.connect(self.__window.cmdDeleteSong, QtCore.SIGNAL('clicked()'), self.cmdDeleteSong_clicked)
#         QtCore.QObject.connect(self.__window.cmdRefreshImageView, QtCore.SIGNAL('clicked()'),
#                                self.cmdRefreshImageView_clicked)
#         QtCore.QObject.connect(self.__window.cmdCompactView, QtCore.SIGNAL('toggled(bool)'),
#                                self.cmdCompactView_toggled)

#         QtCore.QObject.connect(self.__window.cmdDirectToLive, QtCore.SIGNAL('toggled(bool)'),
#                                self.cmdDirectToLive_toggled)

#         QtCore.QObject.connect(self.__window.cmdGotoLive, QtCore.SIGNAL('clicked()'),
#                                self.cmdGotoLive_clicked)

#     def set_status(self, msg, error=False, time_to_hide=None, msg_after_hide=''):
#         pixmap = QtGui.QPixmap(":/main/icons/{0}.png".format("error-24" if error else "valid-24"))

#         self.__window.lblGeneralStatus.setText(msg.capitalize())
#         self.__window.lblStatusIcon.setVisible(True)
#         self.__window.lblStatusIcon.setPixmap(pixmap)

#         if time_to_hide:
#             def worker():
#                 time.sleep(time_to_hide)
#                 self.__window.lblGeneralStatus.setText(msg_after_hide)
#                 self.__window.lblStatusIcon.setVisible(True if msg_after_hide else False)

#             thread = threading.Thread(target=worker)
#             thread.start()

#     def set_in_live(self, in_live):

#         self.in_live = in_live

#         self.__window.cmdFullScreen.setChecked(False)
#         self.__window.cmdDirectToLive.setChecked(False)

#         self.__window.cmdDirectToLive.setEnabled(in_live)
#         self.__window.cmdGotoLive.setEnabled(in_live)
#         self.__window.cmdMainView.setEnabled(in_live)
#         self.__window.cmdColorScreen.setEnabled(in_live)
#         self.__window.cmdFullScreen.setEnabled(in_live)
#         self.__window.cbLiveIn.setEnabled(not in_live)

#         self.__window.lblButton.setText('')

#         self.full_screen.set_visible(in_live, self.__window.cbLiveIn.currentIndex() + 1)
#         self.__window.lblLive.setEnabled(in_live)
#         self.__window.lblLive.setStyleSheet('color: rgb(255, 0, 0);' if in_live else '')

#         if in_live:
#             self.full_screen.set_color(Qt.red)

#         else:
#             self.__window.cmdPrevious.setEnabled(False)
#             self.__window.cmdNext.setEnabled(False)
#             self.__window.cmdLive.setChecked(False)

#         self.set_status('In live' if in_live else 'Off live')

#         self.set_seeker()

#     def set_buttons_slides(self, max_slides):
#         self.remove_buttons_slides()

#         cols = 5
#         for slide in range(1, max_slides + 1):
#             button = QtGui.QPushButton(str(slide))

#             button.setMaximumSize(QtCore.QSize(30, 30))
#             button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

#             button.clicked.connect(partial(self.onBtnSlide_clicked, slide))

#             items = self.__window.cmdSlides.count()
#             row = items / cols
#             col = items % cols

#             self.__window.cmdSlides.addWidget(button, row, col)

#     def remove_buttons_slides(self):

#         for index in range(0, self.__window.cmdSlides.count() + 1):
#             row, col, rspan, cspan = self.__window.cmdSlides.getItemPosition(index)
#             item = self.__window.cmdSlides.itemAtPosition(row, col)

#             if item:
#                 item.widget().deleteLater()

#     def set_slides(self, whole_text, delimiter, limit=conf.getint('BIBLE', 'FORWARD_LIMIT')):

#         if self.__window.chkSearchForward.isChecked():
#             splitted = whole_text.split(delimiter)[:limit]
#         else:
#             splitted = whole_text.split(delimiter)

#         self.slides = filter(lambda s: s and s != '(END)', splitted)
#         self.slide_length = len(self.slides)
#         self.slide_position = 0

#         self.set_seeker()

#     def set_seeker(self):
#         self.remove_buttons_slides()

#         if self.in_live and self.slide_length > 1:
#             self.set_buttons_slides(self.slide_length)

#             self.__window.cmdPrevious.setEnabled(False)
#             self.__window.cmdNext.setEnabled(True)

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

#     def txtSearch_enter_pressed(self):
#         text = self.__window.txtSearch.text()
#         result = ''
#         delimiter = ''

#         self.set_status('Ready')

#         if self.__window.rbBible.isChecked():
#             if self.__window.chkSearchForward.isChecked():
#                 text = '{0}-'.format(text)

#             delimiter = bible.DELIMITER
#             try:
#                 result = bible.search_verse(text)
#             except bible.BibleError, e:
#                 self.set_status(str(e), True)

#         else:
#             delimiter = songs.DELIMITER

#             try:
#                 self.selected_song = self.__window.txtSearch.completer().model().selected()
#                 result = self.selected_song.body

#                 self.__window.cmdEditSong.setEnabled(True)
#                 self.__window.cmdDeleteSong.setEnabled(True)
#             except songs.SongError, e:
#                 self.set_status(str(e), True)

#         self.set_slides(result, delimiter)

#         self.__window.txtPreview.setText(result)

#         if self.direct_live:
#             self.full_screen.set_text(self.slides[self.slide_position],
#                                       self.__window.sLiveFont.value())

#     def cmdRefreshImageView_clicked(self):

#         model = ImagesViewModel(get_images_view(), self.__window.cbImagesView)
#         self.__window.cbImagesView.setModel(model)

#     def rbBible_clicked(self):
#         self.__window.txtSearch.setPlaceholderText('Search in bible (F3)')
#         self.__window.txtSearch.setCompleter(None)

#         self.__window.txtSearch.selectAll()
#         self.__window.txtSearch.setFocus()

#         self.__window.cmdEditSong.setEnabled(False)
#         self.__window.cmdDeleteSong.setEnabled(False)
#         self.selected_song = None

#         self.set_status('Bible search')

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

#     def cmdFullScreen_toggled(self, active):
#         self.full_screen.set_full_screen(active)

#         self.__window.lblFullScreen.setEnabled(active)
#         self.__window.lblFullScreen.setStyleSheet('color: rgb(0, 0, 255);' if active else '')

#     def cmdMainView_clicked(self):
#         try:

#             self.full_screen.set_image(self.__window.cbImagesView.model().selected())

#             self.__window.lblButton.setText('Main View')
#             self.set_status('Live in Main View')
#         except ProjectionError, e:
#             self.set_status(str(e), True)

#     def cmdColorScreen_clicked(self):
#         self.full_screen.set_color()

#         self.__window.lblButton.setText(conf.get('LIVE', 'DEFAULT_COLOR').upper())
#         self.set_status('Live in Black')

#     def cmdDirectToLive_toggled(self, active):
#         self.direct_live = active
#         self.set_status('Direct live {0}'.format('on' if active else 'off'))

#     def cmdGotoLive_clicked(self):
#         text = self.__window.txtPreview.toPlainText()

#         if text:
#             self.full_screen.set_text(self.slides[self.slide_position],
#                                       self.__window.sLiveFont.value())

#             if self.in_live:
#                 self.set_seeker()

#         self.set_status('View refreshed')

#     def cmdPrevious_clicked(self):

#         self.slide_position -= 1
#         self.full_screen.set_text(self.slides[self.slide_position],
#                                   self.__window.sLiveFont.value())

#         self.__window.cmdNext.setEnabled(True)
#         self.__window.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

#     def cmdNext_clicked(self):

#         self.slide_position += 1
#         self.full_screen.set_text(self.slides[self.slide_position],
#                                   self.__window.sLiveFont.value())

#         self.__window.cmdPrevious.setEnabled(True)
#         self.__window.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)

#     def onBtnSlide_clicked(self, button_num):

#         self.slide_position = button_num - 1
#         self.full_screen.set_text(self.slides[self.slide_position],
#                                   self.__window.sLiveFont.value())

#         self.__window.sLiveFont.setValue(
#             int(dict(conf.items('FONT_LIVE')).get('size', conf.get('LIVE', 'DEFAULT_FONT_SIZE'))))

#         self.__window.cmdNext.setEnabled(False if self.slide_position == (self.slide_length - 1) else True)
#         self.__window.cmdPrevious.setEnabled(False if self.slide_position == 0 else True)

#     def cmdCompactView_toggled(self, active):
#         n_active = not active

#         self.__window.dockProjectionsTools.setVisible(n_active)
#         self.__window.txtPreview.setVisible(n_active)

#         if active:
#             self.__window.dockProjectionsControls.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
#             self.resize(self.__window.dockProjectionsControls.minimumWidth(), self.default_frame_size.height())
#             self.setWindowFlags(Qt.WindowTitleHint and Qt.WindowStaysOnTopHint)
#             self.show()
#         else:
#             self.__window.dockProjectionsControls.setFeatures(
#                 QtGui.QDockWidget.DockWidgetFloatable or QtGui.QDockWidget.DockWidgetMovable)
#             self.resize(self.default_frame_size)
#             self.setWindowFlags(Qt.WindowShadeButtonHint)
#             self.show()

#         self.set_status('Compact view {0}'.format('on' if active else 'off'))

#     def sLiveFont_valueChanged(self, value):

#         if self.in_live:
#             try:
#                 self.full_screen.set_text(self.slides[self.slide_position], value)
#             except IndexError:
#                 pass

#         self.set_status('Font size: {0} point(s)'.format(value), time_to_hide=2)

#     def keyPressEvent(self, e):

#         if e.key() == Qt.Key_F3:
#             self.__window.txtSearch.selectAll()
#             self.__window.txtSearch.setFocus()

#     def closeEvent(self, e):
#         self.full_screen.set_visible(False)
#         self.full_screen.hide()


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



# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'karaoke/options.ui'
#
# Created: Tue Oct  7 07:43:57 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_options(object):
    def setupUi(self, options):
        options.setObjectName(_fromUtf8("options"))
        options.resize(358, 333)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(options.sizePolicy().hasHeightForWidth())
        options.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(options)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lstSongs = QtGui.QTableWidget(options)
        self.lstSongs.setProperty("showDropIndicator", False)
        self.lstSongs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.lstSongs.setShowGrid(False)
        self.lstSongs.setGridStyle(QtCore.Qt.SolidLine)
        self.lstSongs.setColumnCount(3)
        self.lstSongs.setObjectName(_fromUtf8("lstSongs"))
        self.lstSongs.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.lstSongs.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.lstSongs.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.lstSongs.setHorizontalHeaderItem(2, item)
        self.lstSongs.horizontalHeader().setVisible(False)
        self.lstSongs.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.lstSongs)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cmdAddSong = QtGui.QPushButton(options)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/add-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdAddSong.setIcon(icon)
        self.cmdAddSong.setObjectName(_fromUtf8("cmdAddSong"))
        self.horizontalLayout.addWidget(self.cmdAddSong)
        self.cmdEditSong = QtGui.QPushButton(options)
        self.cmdEditSong.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/edit-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdEditSong.setIcon(icon1)
        self.cmdEditSong.setObjectName(_fromUtf8("cmdEditSong"))
        self.horizontalLayout.addWidget(self.cmdEditSong)
        self.cmdDeleteSong = QtGui.QPushButton(options)
        self.cmdDeleteSong.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/delete-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdDeleteSong.setIcon(icon2)
        self.cmdDeleteSong.setObjectName(_fromUtf8("cmdDeleteSong"))
        self.horizontalLayout.addWidget(self.cmdDeleteSong)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(options)
        QtCore.QMetaObject.connectSlotsByName(options)

    def retranslateUi(self, options):
        options.setWindowTitle(_translate("options", "Form", None))
        item = self.lstSongs.horizontalHeaderItem(0)
        item.setText(_translate("options", "ID", None))
        item = self.lstSongs.horizontalHeaderItem(1)
        item.setText(_translate("options", "Song", None))
        item = self.lstSongs.horizontalHeaderItem(2)
        item.setText(_translate("options", "Artist", None))
        self.cmdAddSong.setText(_translate("options", "Add song", None))
        self.cmdEditSong.setText(_translate("options", "Edit song", None))
        self.cmdDeleteSong.setText(_translate("options", "Delete song", None))

import resources_rc

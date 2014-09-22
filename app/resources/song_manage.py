# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'song_manage.ui'
#
# Created: Thu May 08 10:10:53 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_frmSongManagement(object):
    def setupUi(self, frmSongManagement):
        frmSongManagement.setObjectName(_fromUtf8("frmSongManagement"))
        frmSongManagement.setWindowModality(QtCore.Qt.NonModal)
        frmSongManagement.resize(695, 463)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/songs-32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmSongManagement.setWindowIcon(icon)
        frmSongManagement.setModal(True)
        self.horizontalLayout = QtGui.QHBoxLayout(frmSongManagement)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(frmSongManagement)
        self.label_2.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cbArtist = QtGui.QComboBox(frmSongManagement)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbArtist.sizePolicy().hasHeightForWidth())
        self.cbArtist.setSizePolicy(sizePolicy)
        self.cbArtist.setMinimumSize(QtCore.QSize(200, 0))
        self.cbArtist.setObjectName(_fromUtf8("cbArtist"))
        self.horizontalLayout_2.addWidget(self.cbArtist)
        self.cmdAddArtist = QtGui.QToolButton(frmSongManagement)
        self.cmdAddArtist.setEnabled(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/add-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdAddArtist.setIcon(icon1)
        self.cmdAddArtist.setObjectName(_fromUtf8("cmdAddArtist"))
        self.horizontalLayout_2.addWidget(self.cmdAddArtist)
        self.cmdEditArtist = QtGui.QToolButton(frmSongManagement)
        self.cmdEditArtist.setEnabled(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/edit-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdEditArtist.setIcon(icon2)
        self.cmdEditArtist.setObjectName(_fromUtf8("cmdEditArtist"))
        self.horizontalLayout_2.addWidget(self.cmdEditArtist)
        self.cmdDeleteArtist = QtGui.QToolButton(frmSongManagement)
        self.cmdDeleteArtist.setEnabled(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/delete-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdDeleteArtist.setIcon(icon3)
        self.cmdDeleteArtist.setObjectName(_fromUtf8("cmdDeleteArtist"))
        self.horizontalLayout_2.addWidget(self.cmdDeleteArtist)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        self.label = QtGui.QLabel(frmSongManagement)
        self.label.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtTitle = QtGui.QLineEdit(frmSongManagement)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.gridLayout.addWidget(self.txtTitle, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblStatus = QtGui.QLabel(frmSongManagement)
        self.lblStatus.setText(_fromUtf8(""))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.horizontalLayout_3.addWidget(self.lblStatus)
        self.buttonBox = QtGui.QDialogButtonBox(frmSongManagement)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(frmSongManagement)
        QtCore.QMetaObject.connectSlotsByName(frmSongManagement)

    def retranslateUi(self, frmSongManagement):
        frmSongManagement.setWindowTitle(_translate("frmSongManagement", "Songs", None))
        self.label_2.setText(_translate("frmSongManagement", "Artist", None))
        self.cmdAddArtist.setToolTip(_translate("frmSongManagement", "Add artist", None))
        self.cmdAddArtist.setText(_translate("frmSongManagement", "...", None))
        self.cmdEditArtist.setToolTip(_translate("frmSongManagement", "Edit artist", None))
        self.cmdEditArtist.setText(_translate("frmSongManagement", "...", None))
        self.cmdDeleteArtist.setToolTip(_translate("frmSongManagement", "Delete artist", None))
        self.cmdDeleteArtist.setText(_translate("frmSongManagement", "...", None))
        self.label.setText(_translate("frmSongManagement", "Title", None))

import resources_rc

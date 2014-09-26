# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'management.ui'
#
# Created: Fri Sep 26 17:58:24 2014
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

class Ui_songManagement(object):
    def setupUi(self, songManagement):
        songManagement.setObjectName(_fromUtf8("songManagement"))
        songManagement.resize(667, 522)
        songManagement.setModal(False)
        songManagement.setWizardStyle(QtGui.QWizard.AeroStyle)
        songManagement.setOptions(QtGui.QWizard.NoBackButtonOnStartPage)
        self.wizardPage1 = QtGui.QWizardPage()
        self.wizardPage1.setObjectName(_fromUtf8("wizardPage1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.wizardPage1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.wizardPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtTitle = QtGui.QLineEdit(self.wizardPage1)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.gridLayout.addWidget(self.txtTitle, 0, 1, 1, 7)
        self.cmdDeleteArtist = QtGui.QToolButton(self.wizardPage1)
        self.cmdDeleteArtist.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/delete-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdDeleteArtist.setIcon(icon)
        self.cmdDeleteArtist.setObjectName(_fromUtf8("cmdDeleteArtist"))
        self.gridLayout.addWidget(self.cmdDeleteArtist, 6, 7, 1, 1)
        self.cmdAddArtist = QtGui.QToolButton(self.wizardPage1)
        self.cmdAddArtist.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/add-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdAddArtist.setIcon(icon1)
        self.cmdAddArtist.setObjectName(_fromUtf8("cmdAddArtist"))
        self.gridLayout.addWidget(self.cmdAddArtist, 6, 5, 1, 1)
        self.cmdEditArtist = QtGui.QToolButton(self.wizardPage1)
        self.cmdEditArtist.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/edit-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdEditArtist.setIcon(icon2)
        self.cmdEditArtist.setObjectName(_fromUtf8("cmdEditArtist"))
        self.gridLayout.addWidget(self.cmdEditArtist, 6, 6, 1, 1)
        self.label_2 = QtGui.QLabel(self.wizardPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txtSearchArtist = QtGui.QLineEdit(self.wizardPage1)
        self.txtSearchArtist.setObjectName(_fromUtf8("txtSearchArtist"))
        self.gridLayout.addWidget(self.txtSearchArtist, 6, 0, 1, 5)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.lstArtists = QtGui.QListWidget(self.wizardPage1)
        self.lstArtists.setObjectName(_fromUtf8("lstArtists"))
        self.verticalLayout_2.addWidget(self.lstArtists)
        songManagement.addPage(self.wizardPage1)
        self.wizardPage2 = QtGui.QWizardPage()
        self.wizardPage2.setObjectName(_fromUtf8("wizardPage2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.wizardPage2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_3 = QtGui.QLabel(self.wizardPage2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_4.addWidget(self.label_3)
        self.txtSongBody = QtGui.QTextEdit(self.wizardPage2)
        self.txtSongBody.setObjectName(_fromUtf8("txtSongBody"))
        self.verticalLayout_4.addWidget(self.txtSongBody)
        songManagement.addPage(self.wizardPage2)

        self.retranslateUi(songManagement)
        QtCore.QMetaObject.connectSlotsByName(songManagement)
        songManagement.setTabOrder(self.txtTitle, self.txtSearchArtist)
        songManagement.setTabOrder(self.txtSearchArtist, self.cmdAddArtist)
        songManagement.setTabOrder(self.cmdAddArtist, self.cmdEditArtist)
        songManagement.setTabOrder(self.cmdEditArtist, self.cmdDeleteArtist)
        songManagement.setTabOrder(self.cmdDeleteArtist, self.txtSongBody)

    def retranslateUi(self, songManagement):
        songManagement.setWindowTitle(_translate("songManagement", "Wizard", None))
        self.label.setText(_translate("songManagement", "Title", None))
        self.label_2.setText(_translate("songManagement", "Artist", None))
        self.txtSearchArtist.setPlaceholderText(_translate("songManagement", "Search for name...", None))
        self.label_3.setText(_translate("songManagement", "Body", None))

import resources_rc

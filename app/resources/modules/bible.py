# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bible.ui'
#
# Created: Thu Jan  8 22:33:30 2015
#      by: PyQt4 UI code generator 4.11.1
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

class Ui_bibleOptions(object):
    def setupUi(self, bibleOptions):
        bibleOptions.setObjectName(_fromUtf8("bibleOptions"))
        bibleOptions.resize(817, 440)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(bibleOptions.sizePolicy().hasHeightForWidth())
        bibleOptions.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(bibleOptions)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmdPrevChapter = QtGui.QPushButton(bibleOptions)
        self.cmdPrevChapter.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdPrevChapter.sizePolicy().hasHeightForWidth())
        self.cmdPrevChapter.setSizePolicy(sizePolicy)
        self.cmdPrevChapter.setStatusTip(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/book-26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdPrevChapter.setIcon(icon)
        self.cmdPrevChapter.setIconSize(QtCore.QSize(26, 26))
        self.cmdPrevChapter.setObjectName(_fromUtf8("cmdPrevChapter"))
        self.gridLayout.addWidget(self.cmdPrevChapter, 1, 0, 1, 1)
        self.cmdPrevVerse = QtGui.QPushButton(bibleOptions)
        self.cmdPrevVerse.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdPrevVerse.sizePolicy().hasHeightForWidth())
        self.cmdPrevVerse.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/verse-24.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdPrevVerse.setIcon(icon1)
        self.cmdPrevVerse.setIconSize(QtCore.QSize(24, 24))
        self.cmdPrevVerse.setFlat(False)
        self.cmdPrevVerse.setObjectName(_fromUtf8("cmdPrevVerse"))
        self.gridLayout.addWidget(self.cmdPrevVerse, 2, 0, 1, 1)
        self.cmdNextVerse = QtGui.QPushButton(bibleOptions)
        self.cmdNextVerse.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdNextVerse.sizePolicy().hasHeightForWidth())
        self.cmdNextVerse.setSizePolicy(sizePolicy)
        self.cmdNextVerse.setIcon(icon1)
        self.cmdNextVerse.setIconSize(QtCore.QSize(26, 26))
        self.cmdNextVerse.setObjectName(_fromUtf8("cmdNextVerse"))
        self.gridLayout.addWidget(self.cmdNextVerse, 2, 1, 1, 1)
        self.cmdNextChapter = QtGui.QPushButton(bibleOptions)
        self.cmdNextChapter.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdNextChapter.sizePolicy().hasHeightForWidth())
        self.cmdNextChapter.setSizePolicy(sizePolicy)
        self.cmdNextChapter.setStatusTip(_fromUtf8(""))
        self.cmdNextChapter.setIcon(icon)
        self.cmdNextChapter.setIconSize(QtCore.QSize(26, 26))
        self.cmdNextChapter.setFlat(False)
        self.cmdNextChapter.setObjectName(_fromUtf8("cmdNextChapter"))
        self.gridLayout.addWidget(self.cmdNextChapter, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.chkInternetService = QtGui.QCheckBox(bibleOptions)
        self.chkInternetService.setObjectName(_fromUtf8("chkInternetService"))
        self.verticalLayout.addWidget(self.chkInternetService)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(bibleOptions)
        QtCore.QMetaObject.connectSlotsByName(bibleOptions)

    def retranslateUi(self, bibleOptions):
        bibleOptions.setWindowTitle(_translate("bibleOptions", "Form", None))
        self.cmdPrevChapter.setToolTip(_translate("bibleOptions", "Previous Chapter", None))
        self.cmdPrevChapter.setText(_translate("bibleOptions", "Previous", None))
        self.cmdPrevChapter.setShortcut(_translate("bibleOptions", "Ctrl+PgDown", None))
        self.cmdPrevVerse.setToolTip(_translate("bibleOptions", "Previous Verse", None))
        self.cmdPrevVerse.setText(_translate("bibleOptions", "Previous", None))
        self.cmdPrevVerse.setShortcut(_translate("bibleOptions", "PgDown", None))
        self.cmdNextVerse.setToolTip(_translate("bibleOptions", "Next Verse", None))
        self.cmdNextVerse.setText(_translate("bibleOptions", "Next", None))
        self.cmdNextVerse.setShortcut(_translate("bibleOptions", "PgUp", None))
        self.cmdNextChapter.setToolTip(_translate("bibleOptions", "Next Chapter", None))
        self.cmdNextChapter.setText(_translate("bibleOptions", "Next", None))
        self.cmdNextChapter.setShortcut(_translate("bibleOptions", "Ctrl+PgUp", None))
        self.chkInternetService.setText(_translate("bibleOptions", "Use bible internet service", None))

import resources_rc

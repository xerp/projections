# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bible.ui'
#
# Created: Wed Sep 24 09:23:37 2014
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

class Ui_bibleOptions(object):
    def setupUi(self, bibleOptions):
        bibleOptions.setObjectName(_fromUtf8("bibleOptions"))
        bibleOptions.resize(387, 149)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(bibleOptions.sizePolicy().hasHeightForWidth())
        bibleOptions.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(bibleOptions)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbSearchForward = QtGui.QCheckBox(bibleOptions)
        self.cbSearchForward.setObjectName(_fromUtf8("cbSearchForward"))
        self.verticalLayout.addWidget(self.cbSearchForward)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmdNextChapter = QtGui.QPushButton(bibleOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdNextChapter.sizePolicy().hasHeightForWidth())
        self.cmdNextChapter.setSizePolicy(sizePolicy)
        self.cmdNextChapter.setStatusTip(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/chapter-24.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdNextChapter.setIcon(icon)
        self.cmdNextChapter.setIconSize(QtCore.QSize(26, 26))
        self.cmdNextChapter.setObjectName(_fromUtf8("cmdNextChapter"))
        self.gridLayout.addWidget(self.cmdNextChapter, 1, 1, 1, 1)
        self.cmdPrevChapter = QtGui.QPushButton(bibleOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdPrevChapter.sizePolicy().hasHeightForWidth())
        self.cmdPrevChapter.setSizePolicy(sizePolicy)
        self.cmdPrevChapter.setStatusTip(_fromUtf8(""))
        self.cmdPrevChapter.setIcon(icon)
        self.cmdPrevChapter.setIconSize(QtCore.QSize(26, 26))
        self.cmdPrevChapter.setObjectName(_fromUtf8("cmdPrevChapter"))
        self.gridLayout.addWidget(self.cmdPrevChapter, 0, 1, 1, 1)
        self.cmdPrevBook = QtGui.QPushButton(bibleOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdPrevBook.sizePolicy().hasHeightForWidth())
        self.cmdPrevBook.setSizePolicy(sizePolicy)
        self.cmdPrevBook.setStatusTip(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/book-26.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdPrevBook.setIcon(icon1)
        self.cmdPrevBook.setIconSize(QtCore.QSize(26, 26))
        self.cmdPrevBook.setObjectName(_fromUtf8("cmdPrevBook"))
        self.gridLayout.addWidget(self.cmdPrevBook, 0, 0, 1, 1)
        self.cmdNextBook = QtGui.QPushButton(bibleOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdNextBook.sizePolicy().hasHeightForWidth())
        self.cmdNextBook.setSizePolicy(sizePolicy)
        self.cmdNextBook.setStatusTip(_fromUtf8(""))
        self.cmdNextBook.setIcon(icon1)
        self.cmdNextBook.setIconSize(QtCore.QSize(26, 26))
        self.cmdNextBook.setObjectName(_fromUtf8("cmdNextBook"))
        self.gridLayout.addWidget(self.cmdNextBook, 1, 0, 1, 1)
        self.cmdPrevVerse = QtGui.QPushButton(bibleOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdPrevVerse.sizePolicy().hasHeightForWidth())
        self.cmdPrevVerse.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/verse-24.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdPrevVerse.setIcon(icon2)
        self.cmdPrevVerse.setIconSize(QtCore.QSize(24, 24))
        self.cmdPrevVerse.setFlat(False)
        self.cmdPrevVerse.setObjectName(_fromUtf8("cmdPrevVerse"))
        self.gridLayout.addWidget(self.cmdPrevVerse, 0, 2, 1, 1)
        self.cmdNextVerse = QtGui.QPushButton(bibleOptions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdNextVerse.sizePolicy().hasHeightForWidth())
        self.cmdNextVerse.setSizePolicy(sizePolicy)
        self.cmdNextVerse.setIcon(icon2)
        self.cmdNextVerse.setIconSize(QtCore.QSize(26, 26))
        self.cmdNextVerse.setObjectName(_fromUtf8("cmdNextVerse"))
        self.gridLayout.addWidget(self.cmdNextVerse, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(bibleOptions)
        QtCore.QMetaObject.connectSlotsByName(bibleOptions)

    def retranslateUi(self, bibleOptions):
        bibleOptions.setWindowTitle(_translate("bibleOptions", "Form", None))
        self.cbSearchForward.setText(_translate("bibleOptions", "Search Forward", None))
        self.cmdNextChapter.setToolTip(_translate("bibleOptions", "Next Chapter", None))
        self.cmdNextChapter.setText(_translate("bibleOptions", "Next", None))
        self.cmdPrevChapter.setToolTip(_translate("bibleOptions", "Previous Chapter", None))
        self.cmdPrevChapter.setText(_translate("bibleOptions", "Previous", None))
        self.cmdPrevBook.setToolTip(_translate("bibleOptions", "Previous Book", None))
        self.cmdPrevBook.setText(_translate("bibleOptions", "Previous", None))
        self.cmdNextBook.setToolTip(_translate("bibleOptions", "Next Book", None))
        self.cmdNextBook.setText(_translate("bibleOptions", "Next", None))
        self.cmdPrevVerse.setToolTip(_translate("bibleOptions", "Previous Verse", None))
        self.cmdPrevVerse.setText(_translate("bibleOptions", "Previous", None))
        self.cmdNextVerse.setToolTip(_translate("bibleOptions", "Next Verse", None))
        self.cmdNextVerse.setText(_translate("bibleOptions", "Next", None))

import resources_rc

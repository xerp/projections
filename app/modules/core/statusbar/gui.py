# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statusbar.ui'
#
# Created: Tue Sep 23 17:44:36 2014
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

class Ui_statusBar(object):
    def setupUi(self, statusBar):
        statusBar.setObjectName(_fromUtf8("statusBar"))
        statusBar.resize(728, 45)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(statusBar.sizePolicy().hasHeightForWidth())
        statusBar.setSizePolicy(sizePolicy)
        statusBar.setMinimumSize(QtCore.QSize(0, 28))
        statusBar.setMaximumSize(QtCore.QSize(16777215, 45))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(statusBar)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblStatusIcon = QtGui.QLabel(statusBar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblStatusIcon.sizePolicy().hasHeightForWidth())
        self.lblStatusIcon.setSizePolicy(sizePolicy)
        self.lblStatusIcon.setMinimumSize(QtCore.QSize(0, 25))
        self.lblStatusIcon.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblStatusIcon.setText(_fromUtf8(""))
        self.lblStatusIcon.setPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/valid-24.png")))
        self.lblStatusIcon.setScaledContents(False)
        self.lblStatusIcon.setIndent(0)
        self.lblStatusIcon.setObjectName(_fromUtf8("lblStatusIcon"))
        self.horizontalLayout.addWidget(self.lblStatusIcon)
        self.lblGeneralStatus = QtGui.QLabel(statusBar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblGeneralStatus.sizePolicy().hasHeightForWidth())
        self.lblGeneralStatus.setSizePolicy(sizePolicy)
        self.lblGeneralStatus.setText(_fromUtf8(""))
        self.lblGeneralStatus.setTextFormat(QtCore.Qt.LogText)
        self.lblGeneralStatus.setIndent(10)
        self.lblGeneralStatus.setObjectName(_fromUtf8("lblGeneralStatus"))
        self.horizontalLayout.addWidget(self.lblGeneralStatus)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lblButton = QtGui.QLabel(statusBar)
        self.lblButton.setText(_fromUtf8(""))
        self.lblButton.setObjectName(_fromUtf8("lblButton"))
        self.horizontalLayout.addWidget(self.lblButton)
        self.line_5 = QtGui.QFrame(statusBar)
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.horizontalLayout.addWidget(self.line_5)
        self.lblFullScreen = QtGui.QLabel(statusBar)
        self.lblFullScreen.setEnabled(False)
        self.lblFullScreen.setObjectName(_fromUtf8("lblFullScreen"))
        self.horizontalLayout.addWidget(self.lblFullScreen)
        self.line_4 = QtGui.QFrame(statusBar)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.horizontalLayout.addWidget(self.line_4)
        self.lblLive = QtGui.QLabel(statusBar)
        self.lblLive.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblLive.setFont(font)
        self.lblLive.setObjectName(_fromUtf8("lblLive"))
        self.horizontalLayout.addWidget(self.lblLive)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(statusBar)
        QtCore.QMetaObject.connectSlotsByName(statusBar)

    def retranslateUi(self, statusBar):
        statusBar.setWindowTitle(_translate("statusBar", "Form", None))
        self.lblFullScreen.setText(_translate("statusBar", "FullScreen", None))
        self.lblLive.setText(_translate("statusBar", "LIVE", None))

import resources_rc

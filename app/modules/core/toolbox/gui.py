# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolbox.ui'
#
# Created: Tue Sep 23 17:16:17 2014
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


class Ui_dockProjectionsTools(object):

    def setupUi(self, dockProjectionsTools):
        dockProjectionsTools.setObjectName(_fromUtf8("dockProjectionsTools"))
        dockProjectionsTools.resize(844, 78)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            dockProjectionsTools.sizePolicy().hasHeightForWidth())
        dockProjectionsTools.setSizePolicy(sizePolicy)
        dockProjectionsTools.setMaximumSize(QtCore.QSize(524287, 78))
        dockProjectionsTools.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        dockProjectionsTools.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        dockProjectionsTools.setWindowTitle(_fromUtf8("Projection Tools"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setText(_fromUtf8("Options"))
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setIndent(-2)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.cbOptions = QtGui.QComboBox(self.dockWidgetContents)
        self.cbOptions.setObjectName(_fromUtf8("cbOptions"))
        self.horizontalLayout_4.addWidget(self.cbOptions)
        self.line_4 = QtGui.QFrame(self.dockWidgetContents)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.horizontalLayout_4.addWidget(self.line_4)
        self.cmdGotoLive = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdGotoLive.setEnabled(False)
        self.cmdGotoLive.setCheckable(False)
        self.cmdGotoLive.setChecked(False)
        self.cmdGotoLive.setAutoRepeat(False)
        self.cmdGotoLive.setAutoExclusive(False)
        self.cmdGotoLive.setAutoRepeatDelay(1)
        self.cmdGotoLive.setAutoRepeatInterval(1)
        self.cmdGotoLive.setFlat(False)
        self.cmdGotoLive.setObjectName(_fromUtf8("cmdGotoLive"))
        self.horizontalLayout_4.addWidget(self.cmdGotoLive)
        self.cmdDirectToLive = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdDirectToLive.setEnabled(False)
        self.cmdDirectToLive.setCheckable(True)
        self.cmdDirectToLive.setObjectName(_fromUtf8("cmdDirectToLive"))
        self.horizontalLayout_4.addWidget(self.cmdDirectToLive)
        self.line_2 = QtGui.QFrame(self.dockWidgetContents)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout_4.addWidget(self.line_2)
        self.cmdColorScreen = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdColorScreen.setEnabled(False)
        self.cmdColorScreen.setObjectName(_fromUtf8("cmdColorScreen"))
        self.horizontalLayout_4.addWidget(self.cmdColorScreen)
        self.cmdMainView = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdMainView.setEnabled(False)
        self.cmdMainView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.cmdMainView.setObjectName(_fromUtf8("cmdMainView"))
        self.horizontalLayout_4.addWidget(self.cmdMainView)
        self.cmdFullScreen = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdFullScreen.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(
            ":/main/icons/Fullscreen-64.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cmdFullScreen.setIcon(icon)
        self.cmdFullScreen.setCheckable(True)
        self.cmdFullScreen.setObjectName(_fromUtf8("cmdFullScreen"))
        self.horizontalLayout_4.addWidget(self.cmdFullScreen)
        self.line_3 = QtGui.QFrame(self.dockWidgetContents)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.horizontalLayout_4.addWidget(self.line_3)
        self.cmdLive = QtGui.QPushButton(self.dockWidgetContents)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            _fromUtf8(":/main/icons/Live.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdLive.setIcon(icon1)
        self.cmdLive.setIconSize(QtCore.QSize(28, 28))
        self.cmdLive.setCheckable(True)
        self.cmdLive.setAutoRepeat(False)
        self.cmdLive.setObjectName(_fromUtf8("cmdLive"))
        self.horizontalLayout_4.addWidget(self.cmdLive)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        dockProjectionsTools.setWidget(self.dockWidgetContents)

        self.retranslateUi(dockProjectionsTools)
        QtCore.QMetaObject.connectSlotsByName(dockProjectionsTools)

    def retranslateUi(self, dockProjectionsTools):
        self.cmdGotoLive.setText(_translate(
            "dockProjectionsTools", "Go to Live (F5)", None))
        self.cmdGotoLive.setShortcut(_translate(
            "dockProjectionsTools", "F5", None))
        self.cmdDirectToLive.setText(_translate(
            "dockProjectionsTools", "Direct To Live (F6)", None))
        self.cmdDirectToLive.setShortcut(
            _translate("dockProjectionsTools", "F6", None))
        self.cmdColorScreen.setText(_translate(
            "dockProjectionsTools", "ColorScreen", None))
        self.cmdMainView.setText(_translate(
            "dockProjectionsTools", "Image View (F10)", None))
        self.cmdMainView.setShortcut(_translate(
            "dockProjectionsTools", "F10", None))
        self.cmdFullScreen.setText(_translate(
            "dockProjectionsTools", "Fullscreen (F11)", None))
        self.cmdFullScreen.setShortcut(
            _translate("dockProjectionsTools", "F11", None))
        self.cmdLive.setText(_translate(
            "dockProjectionsTools", "Live (F12)", None))
        self.cmdLive.setShortcut(_translate(
            "dockProjectionsTools", "F12", None))

import resources_rc

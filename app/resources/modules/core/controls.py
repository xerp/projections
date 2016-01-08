# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controls.ui'
#
# Created: Mon Jan 12 14:31:13 2015
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

class Ui_projectionsControls(object):
    def setupUi(self, projectionsControls):
        projectionsControls.setObjectName(_fromUtf8("projectionsControls"))
        projectionsControls.resize(669, 671)
        projectionsControls.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.txtSearch = QtGui.QLineEdit(self.dockWidgetContents)
        self.txtSearch.setMinimumSize(QtCore.QSize(0, 30))
        self.txtSearch.setStyleSheet(_fromUtf8(""))
        self.txtSearch.setInputMask(_fromUtf8(""))
        self.txtSearch.setText(_fromUtf8(""))
        self.txtSearch.setEchoMode(QtGui.QLineEdit.Normal)
        self.txtSearch.setObjectName(_fromUtf8("txtSearch"))
        self.gridLayout_3.addWidget(self.txtSearch, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.cbLiveScreens = QtGui.QComboBox(self.dockWidgetContents)
        self.cbLiveScreens.setObjectName(_fromUtf8("cbLiveScreens"))
        self.horizontalLayout_4.addWidget(self.cbLiveScreens)
        self.cmdRefreshLiveScreens = QtGui.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/refresh-20.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdRefreshLiveScreens.setIcon(icon)
        self.cmdRefreshLiveScreens.setIconSize(QtCore.QSize(20, 20))
        self.cmdRefreshLiveScreens.setObjectName(_fromUtf8("cmdRefreshLiveScreens"))
        self.horizontalLayout_4.addWidget(self.cmdRefreshLiveScreens)
        self.gridLayout.addLayout(self.horizontalLayout_4, 10, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.cmdPrevious = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdPrevious.setEnabled(False)
        self.cmdPrevious.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cmdPrevious.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/Go back.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cmdPrevious.setIcon(icon1)
        self.cmdPrevious.setIconSize(QtCore.QSize(20, 20))
        self.cmdPrevious.setCheckable(False)
        self.cmdPrevious.setChecked(False)
        self.cmdPrevious.setObjectName(_fromUtf8("cmdPrevious"))
        self.horizontalLayout_3.addWidget(self.cmdPrevious)
        self.cmdNext = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdNext.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdNext.sizePolicy().hasHeightForWidth())
        self.cmdNext.setSizePolicy(sizePolicy)
        self.cmdNext.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cmdNext.setAutoFillBackground(False)
        self.cmdNext.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/Go forward.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cmdNext.setIcon(icon2)
        self.cmdNext.setIconSize(QtCore.QSize(20, 20))
        self.cmdNext.setObjectName(_fromUtf8("cmdNext"))
        self.horizontalLayout_3.addWidget(self.cmdNext)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 2)
        self.saCmdSlides = QtGui.QScrollArea(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saCmdSlides.sizePolicy().hasHeightForWidth())
        self.saCmdSlides.setSizePolicy(sizePolicy)
        self.saCmdSlides.setWidgetResizable(True)
        self.saCmdSlides.setObjectName(_fromUtf8("saCmdSlides"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 645, 137))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cmdSlides = QtGui.QGridLayout()
        self.cmdSlides.setObjectName(_fromUtf8("cmdSlides"))
        self.gridLayout_2.addLayout(self.cmdSlides, 0, 0, 1, 1)
        self.saCmdSlides.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.saCmdSlides, 5, 0, 1, 2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.cbImagesView = QtGui.QComboBox(self.dockWidgetContents)
        self.cbImagesView.setObjectName(_fromUtf8("cbImagesView"))
        self.horizontalLayout_7.addWidget(self.cbImagesView)
        self.cmdRefreshImageView = QtGui.QToolButton(self.dockWidgetContents)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/refresh-20.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cmdRefreshImageView.setIcon(icon3)
        self.cmdRefreshImageView.setIconSize(QtCore.QSize(20, 20))
        self.cmdRefreshImageView.setObjectName(_fromUtf8("cmdRefreshImageView"))
        self.horizontalLayout_7.addWidget(self.cmdRefreshImageView)
        self.gridLayout.addLayout(self.horizontalLayout_7, 9, 1, 1, 1)
        self.lblLiveFont = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLiveFont.sizePolicy().hasHeightForWidth())
        self.lblLiveFont.setSizePolicy(sizePolicy)
        self.lblLiveFont.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblLiveFont.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblLiveFont.setIndent(0)
        self.lblLiveFont.setObjectName(_fromUtf8("lblLiveFont"))
        self.gridLayout.addWidget(self.lblLiveFont, 8, 0, 1, 1)
        self.sLiveFont = QtGui.QSlider(self.dockWidgetContents)
        self.sLiveFont.setMinimum(1)
        self.sLiveFont.setMaximum(100)
        self.sLiveFont.setTracking(False)
        self.sLiveFont.setOrientation(QtCore.Qt.Horizontal)
        self.sLiveFont.setTickPosition(QtGui.QSlider.TicksAbove)
        self.sLiveFont.setTickInterval(0)
        self.sLiveFont.setObjectName(_fromUtf8("sLiveFont"))
        self.gridLayout.addWidget(self.sLiveFont, 8, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 10, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 9, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 3, 0, 1, 1)
        self.saModuleOptions = QtGui.QScrollArea(self.dockWidgetContents)
        self.saModuleOptions.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saModuleOptions.sizePolicy().hasHeightForWidth())
        self.saModuleOptions.setSizePolicy(sizePolicy)
        self.saModuleOptions.setWidgetResizable(True)
        self.saModuleOptions.setObjectName(_fromUtf8("saModuleOptions"))
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 647, 273))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.scrollAreaWidgetContents_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.saModuleOptions.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_3.addWidget(self.saModuleOptions, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.cmdPreviousHistory = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdPreviousHistory.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/undo-32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdPreviousHistory.setIcon(icon4)
        self.cmdPreviousHistory.setIconSize(QtCore.QSize(20, 20))
        self.cmdPreviousHistory.setObjectName(_fromUtf8("cmdPreviousHistory"))
        self.horizontalLayout_6.addWidget(self.cmdPreviousHistory)
        self.cmdNextHistory = QtGui.QPushButton(self.dockWidgetContents)
        self.cmdNextHistory.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/redo-32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdNextHistory.setIcon(icon5)
        self.cmdNextHistory.setIconSize(QtCore.QSize(20, 20))
        self.cmdNextHistory.setObjectName(_fromUtf8("cmdNextHistory"))
        self.horizontalLayout_6.addWidget(self.cmdNextHistory)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        projectionsControls.setWidget(self.dockWidgetContents)

        self.retranslateUi(projectionsControls)
        QtCore.QMetaObject.connectSlotsByName(projectionsControls)

    def retranslateUi(self, projectionsControls):
        projectionsControls.setWindowTitle(_translate("projectionsControls", "Projections Control", None))
        self.txtSearch.setToolTip(_translate("projectionsControls", "Search...", None))
        self.txtSearch.setPlaceholderText(_translate("projectionsControls", "Search... (F3)", None))
        self.cmdRefreshLiveScreens.setText(_translate("projectionsControls", "...", None))
        self.cmdPrevious.setToolTip(_translate("projectionsControls", "Go to previous slide", None))
        self.cmdPrevious.setShortcut(_translate("projectionsControls", "Ctrl+Left", None))
        self.cmdNext.setToolTip(_translate("projectionsControls", "Go to next slide", None))
        self.cmdNext.setShortcut(_translate("projectionsControls", "Ctrl+Right", None))
        self.cmdRefreshImageView.setToolTip(_translate("projectionsControls", "Refresh Images View List", None))
        self.cmdRefreshImageView.setText(_translate("projectionsControls", "...", None))
        self.lblLiveFont.setText(_translate("projectionsControls", "Live Font", None))
        self.label_3.setText(_translate("projectionsControls", "Live in", None))
        self.label_2.setText(_translate("projectionsControls", "Image View", None))
        self.cmdPreviousHistory.setToolTip(_translate("projectionsControls", "Previous History", None))
        self.cmdNextHistory.setToolTip(_translate("projectionsControls", "Next History", None))

import resources_rc

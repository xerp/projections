# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'web_page.ui'
#
# Created: Wed Oct 15 04:47:23 2014
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 160)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtWebPage = QtGui.QLineEdit(Form)
        self.txtWebPage.setObjectName(_fromUtf8("txtWebPage"))
        self.horizontalLayout.addWidget(self.txtWebPage)
        self.cmdClearText = QtGui.QToolButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdClearText.sizePolicy().hasHeightForWidth())
        self.cmdClearText.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/main/icons/clear-text-20.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdClearText.setIcon(icon)
        self.cmdClearText.setIconSize(QtCore.QSize(20, 20))
        self.cmdClearText.setObjectName(_fromUtf8("cmdClearText"))
        self.horizontalLayout.addWidget(self.cmdClearText)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.youtubeOptions = QtGui.QGroupBox(Form)
        self.youtubeOptions.setFlat(False)
        self.youtubeOptions.setObjectName(_fromUtf8("youtubeOptions"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.youtubeOptions)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chkAutoPlay = QtGui.QCheckBox(self.youtubeOptions)
        self.chkAutoPlay.setChecked(True)
        self.chkAutoPlay.setObjectName(_fromUtf8("chkAutoPlay"))
        self.horizontalLayout_2.addWidget(self.chkAutoPlay)
        self.chkPlayerControls = QtGui.QCheckBox(self.youtubeOptions)
        self.chkPlayerControls.setChecked(True)
        self.chkPlayerControls.setObjectName(_fromUtf8("chkPlayerControls"))
        self.horizontalLayout_2.addWidget(self.chkPlayerControls)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.youtubeOptions)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Web Page", None))
        self.cmdClearText.setText(_translate("Form", "...", None))
        self.youtubeOptions.setTitle(_translate("Form", "Youtube Options", None))
        self.chkAutoPlay.setText(_translate("Form", "Auto play", None))
        self.chkPlayerControls.setText(_translate("Form", "Player controls", None))

import resources_rc

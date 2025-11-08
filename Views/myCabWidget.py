# -*- coding: utf-8 -*-
# @Time   : 2024/12/26 13:53
# @Author : WWEE
# @File   : myCabWidget.py
from PyQt5 import QtWidgets, QtCore, QtGui


class MyCabWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("")
        self.setObjectName("cab_W")
        self.cab_video_lbl = QtWidgets.QLabel(self)
        self.cab_video_lbl.setGeometry(QtCore.QRect(80, 90, 970, 600))
        self.cab_video_lbl.setStyleSheet("border-radius:10px;\n"
                                         "background-color: rgb(17, 17, 17);")
        self.cab_video_lbl.setObjectName("cab_video_lbl")
        self.cab_reminder_lbl = QtWidgets.QLabel(self)
        self.cab_reminder_lbl.setGeometry(QtCore.QRect(380, 0, 101, 31))
        self.cab_reminder_lbl.setStyleSheet("color: rgb(255, 165, 19);\n"
                                            "font: 87 12pt \"Arial Black\";")
        self.cab_reminder_lbl.setObjectName("cab_reminder_lbl")
        self.cab_record_btn = QtWidgets.QPushButton(self)
        self.cab_record_btn.setGeometry(QtCore.QRect(550, 720, 51, 51))
        self.cab_record_btn.setStyleSheet("border:none")
        self.cab_record_btn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../icon/cab_record_btn_play_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cab_record_btn.setIcon(icon7)
        self.cab_record_btn.setIconSize(QtCore.QSize(40, 40))
        self.cab_record_btn.setObjectName("cab_record_begin_btn")

        _translate = QtCore.QCoreApplication.translate
        self.cab_video_lbl.setText(_translate("Form", "我是cabW，00000000"))
        self.cab_reminder_lbl.setText(_translate("Form", "左顾右盼"))

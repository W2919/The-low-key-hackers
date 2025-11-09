# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 14:02
# @Author : WWEE
# @File   : myTakePhotoWidget.py
from PyQt5 import QtCore, QtWidgets, QtGui


class MyTakePhotoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()
    def init_UI(self):
        self.setObjectName("t_photo_W")
        self.t_photo_capture_lbl = QtWidgets.QLabel(self)
        self.t_photo_capture_lbl.setGeometry(QtCore.QRect(80, 90, 970, 550))
        self.t_photo_capture_lbl.setStyleSheet("border-radius:10px;\n"
                                               "background-color: rgb(20, 20, 20);")
        self.t_photo_capture_lbl.setText("")
        self.t_photo_capture_lbl.setObjectName("t_photo_capture_lbl")
        self.t_photo_show_lbl = QtWidgets.QLabel(self)
        self.t_photo_show_lbl.setGeometry(QtCore.QRect(900, 640, 221, 131))
        self.t_photo_show_lbl.setStyleSheet("")
        self.t_photo_show_lbl.setText("")
        self.t_photo_show_lbl.setObjectName("t_photo_show_lbl")
        self.t_photo_take_photo_btn = QtWidgets.QPushButton(self)
        self.t_photo_take_photo_btn.setGeometry(QtCore.QRect(530, 690, 91, 51))
        self.t_photo_take_photo_btn.setStyleSheet("border: none;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/road_screenshot_btn_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.t_photo_take_photo_btn.setIcon(icon)
        self.t_photo_take_photo_btn.setIconSize(QtCore.QSize(40, 40))
        self.t_photo_take_photo_btn.setObjectName("t_photo_take_photo_btn")

        _translate = QtCore.QCoreApplication.translate

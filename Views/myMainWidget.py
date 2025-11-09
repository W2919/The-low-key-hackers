# -*- coding: utf-8 -*-
# @Time   : 2025/1/12 11:55
# @Author : WWEE
# @File   : myMainWidget.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget


class MyMainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        # self.main_W = QtWidgets.QWidget()
        self.setObjectName("main_W")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(150, 130, 841, 481))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../resource/icon/mainWin_background_lbl_img.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
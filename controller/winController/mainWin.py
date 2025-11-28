# -*- coding: utf-8 -*-
# @Time   : 2025/1/12 11:57
# @Author : WWEE
# @File   : appMainWin.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QHBoxLayout

from Views.myMainWidget import MyMainWidget

class mainWin(MyMainWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(70, 80, 991, 631))
        self.label.setText("2873901210")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)
        self.label.setPixmap(QtGui.QPixmap(".\\UI\\../resource/icon/mainWin_background_lbl_img.png"))


    def refresh(self):
        pass
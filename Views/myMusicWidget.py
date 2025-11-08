# -*- coding: utf-8 -*-
# @Time   : 2025/2/9 22:52
# @Author : WWEE
# @File   : myMusicWidget.py
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget


class MyMusicWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.music_play_btn = QtWidgets.QPushButton(self)
        self.music_play_btn.setGeometry(QtCore.QRect(530, 700, 75, 41))
        self.music_play_btn.setStyleSheet("border:none")
        self.music_play_btn.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(".\\../resource/icon/video_play_btn_begin_icon.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.music_play_btn.setIcon(icon10)
        self.music_play_btn.setIconSize(QtCore.QSize(40, 40))
        self.music_play_btn.setObjectName("music_play_btn")
        self.music_prev_btn = QtWidgets.QPushButton(self)
        self.music_prev_btn.setGeometry(QtCore.QRect(430, 700, 71, 51))
        self.music_prev_btn.setStyleSheet("border:none;\n"
                                          "color:rgb(87,87,87);\n"
                                          "font: 25pt \"华文琥珀\";")
        self.music_prev_btn.setObjectName("music_prev_btn")
        self.music_show_list = QtWidgets.QListWidget(self)
        self.music_show_list.setGeometry(QtCore.QRect(70, 70, 1001, 571))
        self.music_show_list.setStyleSheet("border-radius:10px;\n"
                                           "background-color: rgb(20, 20, 20);\n"
                                           "color: rgb(127, 127, 127)")
        self.music_show_list.setObjectName("music_show_list")
        self.music_slider = QtWidgets.QSlider(self)
        self.music_slider.setGeometry(QtCore.QRect(69, 660, 1001, 20))
        self.music_slider.setOrientation(QtCore.Qt.Horizontal)
        self.music_slider.setObjectName("music_slider")
        self.music_next_btn = QtWidgets.QPushButton(self)
        self.music_next_btn.setGeometry(QtCore.QRect(630, 700, 71, 51))
        self.music_next_btn.setStyleSheet("border:none;\n"
                                          "color:rgb(87,87,87);\n"
                                          "font: 25pt \"华文琥珀\";")
        self.music_next_btn.setObjectName("music_next_btn")
        self.music_add_btn = QtWidgets.QPushButton(self)
        self.music_add_btn.setGeometry(QtCore.QRect(790, 702, 171, 41))
        self.music_add_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                         "background-color: rgb(68, 64, 67);\n"
                                         "color: rgb(127, 127, 127);\n"
                                         "")
        self.music_add_btn.setObjectName("music_add_btn")

        _translate = QtCore.QCoreApplication.translate
        self.music_prev_btn.setText(_translate("Form", "<<"))
        self.music_next_btn.setText(_translate("Form", ">>"))
        self.music_add_btn.setText(_translate("Form", "添加音频"))
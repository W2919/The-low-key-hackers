# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 18:32
# @Author : WWEE
# @File   : myRoadWidget.py
from PyQt5 import QtWidgets, QtCore, QtGui


class MyRoadWidget(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            self.init_UI()

        def init_UI(self):
            self.setStyleSheet("")
            self.setObjectName("road_W")
            self.road_video_lbl = QtWidgets.QLabel(self)
            self.road_video_lbl.setGeometry(QtCore.QRect(30, 40, 1081, 671))
            self.road_video_lbl.setStyleSheet("border-radius:10px;\n"
                                              "background-color: rgb(20, 20, 20);")
            self.road_video_lbl.setObjectName("road_video_lbl")
            self.road_reminder_lbl = QtWidgets.QLabel(self)
            self.road_reminder_lbl.setGeometry(QtCore.QRect(270, 0, 281, 21))
            self.road_reminder_lbl.setStyleSheet("color: rgb(255, 165, 19);\n"
                                                 "font: 87 12pt \"Arial Black\";")
            self.road_reminder_lbl.setObjectName("road_reminder_lbl")
            self.road_screenshot_btn = QtWidgets.QPushButton(self)
            self.road_screenshot_btn.setGeometry(QtCore.QRect(550, 730, 51, 51))
            self.road_screenshot_btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.road_screenshot_btn.setStyleSheet("border:none")
            self.road_screenshot_btn.setText("")
            # icon8 = QtGui.QIcon()
            # icon8.addPixmap(QtGui.QPixmap("../icon/road_screenshot_btn_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            # self.road_screenshot_btn.setIcon(icon8)
            self.road_screenshot_btn.setIconSize(QtCore.QSize(40, 40))
            self.road_screenshot_btn.setObjectName("road_screenshot_btn")

            _translate = QtCore.QCoreApplication.translate
            self.road_video_lbl.setText(_translate("Form", "我是roadW，11111111"))
            self.road_reminder_lbl.setText(_translate("Form", "左顾右盼"))

# -*- coding: utf-8 -*-
# @Time   : 2024/12/26 0:30
# @Author : WWEE
# @File   : myVideoWidget.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget


class myVideoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("video_W")
        self.video_dateEdit = QtWidgets.QDateEdit(self)
        self.video_dateEdit.setGeometry(QtCore.QRect(10, 30, 130, 25))
        self.video_dateEdit.setStyleSheet("background-color: rgb(35, 35, 35);\n"
                                          "color: rgb(255, 255, 255);"
                                          "border-radius:10px")
        self.video_dateEdit.setObjectName("video_dateEdit")


        self.video_search_btn = QtWidgets.QPushButton(self)
        self.video_search_btn.setGeometry(QtCore.QRect(140, 30, 60, 25))
        self.video_search_btn.setStyleSheet("background-color: rgb(35, 35, 35);\n"
                                            "color: rgb(255, 255, 255);"
                                            "font: 10pt \"华文琥珀\";\n")
        self.video_search_btn.setObjectName("video_search_btn")

        self.video_search_all_btn = QtWidgets.QPushButton(self)
        self.video_search_all_btn.setGeometry(QtCore.QRect(210, 30, 60, 25))
        self.video_search_all_btn.setStyleSheet("background-color: rgb(35, 35, 35);\n"
                                            "color: rgb(255, 255, 255);"
                                            "font: 10pt \"华文琥珀\";\n")
        self.video_search_all_btn.setObjectName("video_search_all_btn")


        self.video_show_lbl = QtWidgets.QLabel(self)
        self.video_show_lbl.setGeometry(QtCore.QRect(260, 50, 850, 650))
        self.video_show_lbl.setStyleSheet("border-radius:10px;\n"
                                          "background-color: rgb(20, 20,20);")
        self.video_show_lbl.setText("")
        self.video_show_lbl.setObjectName("video_show_lbl")
        self.video_play_btn = QtWidgets.QPushButton(self)
        self.video_play_btn.setGeometry(QtCore.QRect(650, 740, 75, 31))
        self.video_play_btn.setStyleSheet("border:none")
        self.video_play_btn.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../icon/video_play_btn_begin_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.video_play_btn.setIcon(icon9)
        self.video_play_btn.setIconSize(QtCore.QSize(40, 40))
        self.video_play_btn.setObjectName("video_play_btn")
        self.horizontalSlider = QtWidgets.QSlider(self)
        self.horizontalSlider.setGeometry(QtCore.QRect(260, 720, 860, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.video_speedx1_box = QtWidgets.QRadioButton(self)
        self.video_speedx1_box.setGeometry(QtCore.QRect(630, 0, 100, 25))
        self.video_speedx1_box.setStyleSheet("border:none;\n"
                                             "font: 10pt \"华文琥珀\";\n"
                                             "color: rgb(127, 127, 127);")
        self.video_speedx1_box.setObjectName("video_speedx1_box")
        self.video_speedx05_box = QtWidgets.QRadioButton(self)
        self.video_speedx05_box.setGeometry(QtCore.QRect(490, 0, 100, 25))
        self.video_speedx05_box.setStyleSheet("border:none;\n"
                                              "font: 10pt \"华文琥珀\";\n"
                                              "color: rgb(127, 127, 127);")
        self.video_speedx05_box.setObjectName("video_speedx05_box")
        self.video_speedx2_box = QtWidgets.QRadioButton(self)
        self.video_speedx2_box.setGeometry(QtCore.QRect(770, 0, 100, 25))
        self.video_speedx2_box.setStyleSheet("border:none;\n"
                                             "font: 10pt \"华文琥珀\";\n"
                                             "color: rgb(127, 127, 127);")
        self.video_speedx2_box.setObjectName("video_speedx2_box")

        self.video_open_btn = QtWidgets.QPushButton(self)
        self.video_open_btn.setGeometry(QtCore.QRect(0, 710, 120, 31))
        self.video_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.video_open_btn.setObjectName("video_open_btn")

        self.video_switch_del_btn = QtWidgets.QPushButton(self)
        self.video_switch_del_btn.setGeometry(QtCore.QRect(135, 710, 120, 31))
        self.video_switch_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                            "background-color: rgb(68, 64, 67);\n"
                                            "color: rgb(127, 127, 127);\n"
                                            "")
        self.video_switch_del_btn.setObjectName("video_del_btn")


        self.video_forward_btn = QtWidgets.QPushButton(self)
        self.video_forward_btn.setGeometry(QtCore.QRect(790, 740, 75, 21))
        self.video_forward_btn.setStyleSheet("border:none;\n"
                                      "font: 15pt \"华文琥珀\";\n"
                                      "color: rgb(127, 127, 127);")
        self.video_forward_btn.setObjectName("pushButton")
        self.video_back_btn = QtWidgets.QPushButton(self)
        self.video_back_btn.setGeometry(QtCore.QRect(500, 740, 75, 23))
        self.video_back_btn.setStyleSheet("border:none;\n"
                                          "font: 15pt \"华文琥珀\";\n"
                                          "color: rgb(127, 127, 127);")
        self.video_back_btn.setObjectName("video_back_btn")
        # self.video_list_view = QtWidgets.QListWidget(self)
        # self.video_list_view.setGeometry(QtCore.QRect(10, 60, 201, 650))
        # self.video_list_view.setStyleSheet("border-radius:10px;\n"
        #                                    "background-color: rgb(20, 20, 20);")
        # self.video_list_view.setObjectName("video_list_view")


        _translate = QtCore.QCoreApplication.translate
        self.video_open_btn.setText(_translate("Form", "添加视频"))
        self.video_switch_del_btn.setText(_translate("Form", "删除视频"))
        self.video_speedx1_box.setText(_translate("Form", "1倍速"))
        self.video_speedx05_box.setText(_translate("Form", "0.5倍速"))
        self.video_speedx2_box.setText(_translate("Form", "2倍速"))
        self.video_forward_btn.setText(_translate("Form", "》》"))
        self.video_back_btn.setText(_translate("Form", "《《 "))
        self.video_search_btn.setText(_translate("From", "搜索"))
        self.video_search_all_btn.setText(_translate("From", "全部"))

    def init_list(self):
        self.video_list_view_normal = QtWidgets.QListWidget(self)
        self.video_list_view_normal.setGeometry(QtCore.QRect(10, 60, 201, 650))
        self.video_list_view_normal.setStyleSheet("border-radius:10px;\n"
                                                  "background-color: rgb(20, 20, 20);\n"
                                                  "color: rgb(255, 255, 255);")
        self.video_list_view_normal.setObjectName("video_list_view_normal")

        self.video_list_view_delete = QtWidgets.QListWidget(self)
        self.video_list_view_delete.setGeometry(QtCore.QRect(10, 60, 201, 650))
        self.video_list_view_delete.setStyleSheet("border-radius:10px;\n"
                                                  "background-color: rgb(20, 20, 20);\n"
                                                  "color: rgb(255, 255, 255);")
        self.video_list_view_delete.setObjectName("video_list_view_delete")

        self.video_open_btn = QtWidgets.QPushButton(self)
        self.video_open_btn.setGeometry(QtCore.QRect(0, 710, 120, 31))
        self.video_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.video_open_btn.setObjectName("video_open_btn")

        self.video_switch_del_btn = QtWidgets.QPushButton(self)
        self.video_switch_del_btn.setGeometry(QtCore.QRect(135, 710, 120, 31))
        self.video_switch_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                                "background-color: rgb(68, 64, 67);\n"
                                                "color: rgb(127, 127, 127);\n"
                                                "")
        self.video_switch_del_btn.setObjectName("video_switch_del_btn")

        self.video_return_btn = QtWidgets.QPushButton(self)
        self.video_return_btn.setGeometry(QtCore.QRect(0, 710, 120, 31))
        self.video_return_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                            "background-color: rgb(68, 64, 67);\n"
                                            "color: rgb(127, 127, 127);\n"
                                            "")
        self.video_return_btn.setObjectName("video_return_btn")

        self.video_del_btn = QtWidgets.QPushButton(self)
        self.video_del_btn.setGeometry(QtCore.QRect(135, 710, 120, 31))
        self.video_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                         "background-color: rgb(68, 64, 67);\n"
                                         "color: rgb(127, 127, 127);\n"
                                         "")
        self.video_del_btn.setObjectName("video_del_btn")

        _translate = QtCore.QCoreApplication.translate
        self.video_open_btn.setText(_translate("Form", "添加视频"))
        self.video_switch_del_btn.setText(_translate("Form", "删除视频"))

        self.video_return_btn.setText(_translate("Form", "返回"))
        self.video_del_btn.setText(_translate("Form", "删除"))

        self.video_open_btn.show()
        self.video_switch_del_btn.show()
        self.video_return_btn.hide()
        self.video_del_btn.hide()

        self.video_list_view_delete.hide()
        self.video_list_view_normal.show()



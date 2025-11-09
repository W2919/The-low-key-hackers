# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 14:59
# @Author : WWEE
# @File   : myPhotoWidget.py
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget


class MyPhotoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setObjectName("photo_W")
        self.photo_show_lbl = QtWidgets.QLabel(self)
        self.photo_show_lbl.setGeometry(QtCore.QRect(230, 10, 850, 660))
        self.photo_show_lbl.setStyleSheet("border-radius:10px;\n"
                                          "background-color: rgb(20, 20, 20);")
        self.photo_show_lbl.setText("")
        self.photo_show_lbl.setObjectName("photo_show_lbl")
        self.photo_single_del_btn = QtWidgets.QPushButton(self)
        self.photo_single_del_btn.setGeometry(QtCore.QRect(620, 740, 111, 31))
        self.photo_single_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                         "background-color: rgb(68, 64, 67);\n"
                                         "color: rgb(127, 127, 127);\n"
                                         "")
        self.photo_single_del_btn.setObjectName("photo_del_btn")
        self.photo_list_view = QtWidgets.QListWidget(self)
        self.photo_list_view.setGeometry(QtCore.QRect(10, 10, 201, 711))
        self.photo_list_view.setStyleSheet("border-radius:10px;\n"
                                           "background-color: rgb(20, 20, 20);\n"
                                           "color: rgb(127, 127, 127);")
        self.photo_list_view.setObjectName("photo_list_view")
        self.photo_next_btn = QtWidgets.QPushButton(self)
        self.photo_next_btn.setGeometry(QtCore.QRect(900, 740, 111, 31))
        self.photo_next_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.photo_next_btn.setObjectName("photo_next_btn")
        self.photo_prev_btn = QtWidgets.QPushButton(self)
        self.photo_prev_btn.setGeometry(QtCore.QRect(330, 740, 111, 31))
        self.photo_prev_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.photo_prev_btn.setObjectName("photo_prev_btn")
        # self.photo_open_btn = QtWidgets.QPushButton(self)
        # self.photo_open_btn.setGeometry(QtCore.QRect(60, 740, 120, 31))
        # self.photo_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
        #                                     "background-color: rgb(68, 64, 67);\n"
        #                                     "color: rgb(127, 127, 127);\n"
        #                                     "")

        # self.photo_open_btn = QtWidgets.QPushButton(self)
        # self.photo_open_btn.setGeometry(QtCore.QRect(0, 730, 120, 31))
        # self.photo_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
        #                                   "background-color: rgb(68, 64, 67);\n"
        #                                   "color: rgb(127, 127, 127);\n"
        #                                   "")
        # self.photo_open_btn.setObjectName("photo_open_btn")
        # self.photo_batch_del_btn = QtWidgets.QPushButton(self)
        # self.photo_batch_del_btn.setGeometry(QtCore.QRect(140, 730, 120, 31))
        # self.photo_batch_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
        #                                        "background-color: rgb(68, 64, 67);\n"
        #                                        "color: rgb(127, 127, 127);\n"
        #                                        "")
        # self.photo_batch_del_btn.setObjectName("photo_batch_del_btn")

        _translate = QtCore.QCoreApplication.translate
        self.photo_single_del_btn.setText(_translate("Form", "删除"))
        self.photo_next_btn.setText(_translate("Form", "下一个"))
        self.photo_prev_btn.setText(_translate("Form", "上一个"))
        # self.photo_open_btn.setText(_translate("Form", "添加照片"))
        # self.photo_batch_del_btn.setText(_translate("Form", "删除照片"))


    def init_list(self):
        self.photo_list_view_normal = QtWidgets.QListWidget(self)
        self.photo_list_view_normal.setGeometry(QtCore.QRect(0, 10, 201, 711))
        self.photo_list_view_normal.setStyleSheet("border-radius:10px;\n"
                                                  "background-color: rgb(20, 20, 20);\n"
                                                  "color: rgb(255, 255, 255);")
        self.photo_list_view_normal.setObjectName("photo_list_view_normal")

        self.photo_list_view_delete = QtWidgets.QListWidget(self)
        self.photo_list_view_delete.setGeometry(QtCore.QRect(0, 10, 201, 711))
        self.photo_list_view_delete.setStyleSheet("border-radius:10px;\n"
                                                  "background-color: rgb(20, 20, 20);\n"
                                                  "color: rgb(255, 255, 255);")
        self.photo_list_view_delete.setObjectName("photo_list_view_delete")

        self.photo_open_btn = QtWidgets.QPushButton(self)
        self.photo_open_btn.setGeometry(QtCore.QRect(0, 730, 120, 31))
        self.photo_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.photo_open_btn.setObjectName("photo_open_btn")

        self.photo_switch_del_btn = QtWidgets.QPushButton(self)
        self.photo_switch_del_btn.setGeometry(QtCore.QRect(140, 730, 120, 31))
        self.photo_switch_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                                "background-color: rgb(68, 64, 67);\n"
                                                "color: rgb(127, 127, 127);\n"
                                                "")
        self.photo_switch_del_btn.setObjectName("photo_switch_del_btn")

        self.photo_return_btn = QtWidgets.QPushButton(self)
        self.photo_return_btn.setGeometry(QtCore.QRect(0, 730, 120, 31))
        self.photo_return_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                            "background-color: rgb(68, 64, 67);\n"
                                            "color: rgb(127, 127, 127);\n"
                                            "")
        self.photo_return_btn.setObjectName("photo_return_btn")

        self.photo_del_btn = QtWidgets.QPushButton(self)
        self.photo_del_btn.setGeometry(QtCore.QRect(140, 730, 120, 31))
        self.photo_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                         "background-color: rgb(68, 64, 67);\n"
                                         "color: rgb(127, 127, 127);\n"
                                         "")
        self.photo_del_btn.setObjectName("photo_del_btn")

        _translate = QtCore.QCoreApplication.translate
        self.photo_open_btn.setText(_translate("Form", "添加照片"))
        self.photo_switch_del_btn.setText(_translate("Form", "删除照片"))

        self.photo_return_btn.setText(_translate("Form", "返回"))
        self.photo_del_btn.setText(_translate("Form", "删除"))

        self.photo_open_btn.show()
        self.photo_switch_del_btn.show()
        self.photo_return_btn.hide()
        self.photo_del_btn.hide()

        self.photo_list_view_delete.hide()
        self.photo_list_view_normal.show()
# -*- coding: utf-8 -*-
# @Time   : 2025/1/5 9:48
# @Author : WWEE
# @File   : myUserWidget.py
from PyQt5 import QtCore
from pyqt5_plugins.examplebutton import QtWidgets


class myUserWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("user_W")
        self.user_img_lbl = QtWidgets.QLabel(self)
        self.user_img_lbl.setGeometry(QtCore.QRect(40, 20, 671, 641))
        self.user_img_lbl.setStyleSheet("border-radius:10px;\n"
                                        "background-color: rgb(20, 20, 20);")
        self.user_img_lbl.setObjectName("user_img_lbl")
        self.user_unm_lbl = QtWidgets.QLabel(self)
        self.user_unm_lbl.setGeometry(QtCore.QRect(740, 50, 150, 61))
        self.user_unm_lbl.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "border:none;\n"
                                        "font: 18pt \"幼圆\";")
        self.user_unm_lbl.setObjectName("user_unm_lbl")
        self.user_phone_lbl = QtWidgets.QLabel(self)
        self.user_phone_lbl.setGeometry(QtCore.QRect(740, 330, 150, 71))
        self.user_phone_lbl.setStyleSheet("color: rgb(255, 255, 255);\n"
                                          "border:none;\n"
                                          "font: 18pt \"幼圆\";")
        self.user_phone_lbl.setObjectName("user_phone_lbl")
        self.user_unmData_lbl = QtWidgets.QLabel(self)
        self.user_unmData_lbl.setGeometry(QtCore.QRect(900, 50, 271, 61))
        self.user_unmData_lbl.setStyleSheet("border:none;\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "font: 20pt \"Agency FB\";")
        self.user_unmData_lbl.setObjectName("user_unmData_lbl")
        self.user_phoneData_lbl = QtWidgets.QLabel(self)
        self.user_phoneData_lbl.setGeometry(QtCore.QRect(900, 330, 271, 71))
        self.user_phoneData_lbl.setStyleSheet("border:none;\n"
                                              "color: rgb(255, 255, 255);\n"
                                              "font: 20pt \"Agency FB\";")
        self.user_phoneData_lbl.setObjectName("user_phoneData_lbl")
        self.user_bind_phone_btn = QtWidgets.QPushButton(self)
        self.user_bind_phone_btn.setGeometry(QtCore.QRect(950, 560, 150, 61))
        self.user_bind_phone_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                               "background-color: rgb(68, 64, 67);\n"
                                               "color: rgb(127, 127, 127);\n"
                                               "")
        self.user_bind_phone_btn.setObjectName("user_bind_phone_btn")
        self.user_upload_img_btn = QtWidgets.QPushButton(self)
        self.user_upload_img_btn.setGeometry(QtCore.QRect(270, 680, 161, 81))
        self.user_upload_img_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                               "background-color: rgb(68, 64, 67);\n"
                                               "color: rgb(127, 127, 127);\n"
                                               "")
        self.user_upload_img_btn.setObjectName("user_upload_img_btn")
        self.user_change_pwd_btn = QtWidgets.QPushButton(self)
        self.user_change_pwd_btn.setGeometry(QtCore.QRect(770, 560, 150, 61))
        self.user_change_pwd_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                               "background-color: rgb(68, 64, 67);\n"
                                               "color: rgb(127, 127, 127);\n"
                                               "")
        self.user_change_pwd_btn.setObjectName("user_change_pwd_btn")

        _translate = QtCore.QCoreApplication.translate
        self.user_unm_lbl.setText(_translate("Form", "用户名:"))
        self.user_phone_lbl.setText(_translate("Form", "电话:"))
        self.user_unmData_lbl.setText(_translate("Form", "WWEE@223"))
        self.user_phoneData_lbl.setText(_translate("Form", "15060058325"))
        self.user_bind_phone_btn.setText(_translate("Form", "绑定新号码"))
        self.user_upload_img_btn.setText(_translate("Form", "上传新头像"))
        self.user_change_pwd_btn.setText(_translate("Form", "修改密码"))

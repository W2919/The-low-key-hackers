# -*- coding: utf-8 -*-
# @Time   : 2024/10/14 16:32
# @Author : WWEE
# @File   : LoginWin.py
# loginFrom.setFixedSize(600, 400)
import os

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtWidgets import QWidget
from controller.LoginController import LoginController
from Views.login import Ui_loginFrom
from models.UserModel import User
import json


class LoginWin(QWidget, Ui_loginFrom):

    switch_window_register = QtCore.pyqtSignal()  # 跳转信号
    switch_window_phone_login = QtCore.pyqtSignal()
    switch_window_mainW = QtCore.pyqtSignal(User)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_icon()
        self.controller = LoginController()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.unm_edit.installEventFilter(self)
        self.pwd_edit.installEventFilter(self)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.goRegister)
        self.phone_login_btn.clicked.connect(self.goPhoneLogin)
        self.view_pwd_btn.clicked.connect(self.chanegPwd_state)
        self.view_pwd_state = False

    def init_icon(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                relative_path = config.get('icon_relative_path')
                self.view_pwd_btn_close_icon = config.get("view_pwd_btn_close_icon")
                self.view_pwd_btn_close_icon = os.path.join(relative_path, config.get("view_pwd_btn_close_icon"))
                self.view_pwd_btn_open_icon = os.path.join(relative_path, config.get("view_pwd_btn_open_icon"))
                self.view_pwd_btn.setIcon(QIcon(self.view_pwd_btn_close_icon))
        except FileNotFoundError:
            print("config.json not found")



    def login(self):
        username = self.unm_edit.text()
        password = self.pwd_edit.text()
        if username == 0 or  password.strip() == '':
            QMessageBox.information(None, "error", "输入不能为空")
        else:
            user = self.controller.handle_pwd_login(username, password)
            print(user)
            if user:
                QMessageBox.information(None, "success","登入成功")
                self.switch_window_mainW.emit(user)
        # user = self.controller.handle_pwd_login("username", "password")
        # print(user)
        # if user:
        #     QMessageBox.information(None, "success", "登入成功")
        #     self.switch_window_mainW.emit(user)

    def showEvent(self, event):
        super().showEvent(event)
        self.unm_edit.setText("")
        self.pwd_edit.setText("")

    def goPhoneLogin(self):
        self.switch_window_phone_login.emit()

    def goRegister(self):
        self.switch_window_register.emit()

    def chanegPwd_state(self):
        if self.view_pwd_state:
            self.view_pwd_state = False
            self.view_pwd_btn.setIcon(QIcon(self.view_pwd_btn_close_icon))
            self.pwd_edit.setEchoMode(QLineEdit.Password)
        else:
            self.view_pwd_state = True
            self.view_pwd_btn.setIcon(QIcon(self.view_pwd_btn_open_icon))
            self.pwd_edit.setEchoMode(QLineEdit.Normal)




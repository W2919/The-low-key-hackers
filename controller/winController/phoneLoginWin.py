# -*- coding: utf-8 -*-
# @Time   : 2025/1/5 17:17
# @Author : WWEE
# @File   : phoneLoginWin.py
import re

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox
from controller.LoginController import LoginController
from Views.phoneLogin import Ui_Form
from models.VerificationCodeModel import VerificationCode
from models.UserModel import User

class phoneLoginWin(QWidget, Ui_Form):

    switch_window_register = QtCore.pyqtSignal()  # 跳转信号
    switch_window_unmPwd_login = QtCore.pyqtSignal()
    switch_window_mainW = QtCore.pyqtSignal(User)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sms_sender = VerificationCode()
        self.controller = LoginController()

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.goRegister)
        self.pwd_login_btn.clicked.connect(self.goUnmPwdLogin)
        self.code_send_btn.clicked.connect(self.sendCode)
        self.count = 30
        self.timer = QTimer()
        self.timer.timeout.connect(self.sendCode_close)

    def login(self):
        phone_number = self.phone_edit.text().strip()
        sms = self.SMS_edit.text().strip()
        if not phone_number or not sms:
            QMessageBox.warning(None, "warning", "相关信息不能为空")
            return

        result = self.controller.handle_phone_login(phone_number, sms, self.code)
        if result:
            self.switch_window_mainW.emit(result)

    def goUnmPwdLogin(self):
        self.switch_window_unmPwd_login.emit()

    def goRegister(self):
        self.switch_window_register.emit()

    def sendCode(self):
        phone_number = self.phone_edit.text()
        if self.controller.user_manager.is_valid_phone_number(phone_number):
            self.code = str(self.sms_sender.send_sms(phone_number))
            # print(self.code)
            self.timer.start(1000)
        else:
            QMessageBox.warning(None, "warning","无效手机号")
        # self.timer.start(1000)

    def sendCode_close(self):
        self.code_send_btn.setEnabled(False)
        self.count = self.count - 1
        self.code_send_btn.setText(str(self.count))
        if self.count == 0:
            self.count = 30
            self.timer.stop()
            self.code_send_btn.setEnabled(True)
            self.code_send_btn.setText("发送")

    def showEvent(self, event):
        super().showEvent(event)
        self.phone_edit.setText("")  # 清空编辑框内容
        self.SMS_edit.setText("")  # 清空编辑框内容

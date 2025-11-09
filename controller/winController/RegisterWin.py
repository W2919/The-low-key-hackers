# -*- coding: utf-8 -*-
# @Time   : 2024/10/14 17:12
# @Author : WWEE
# @File   : RegisterWin.py
import re
#         Register.setFixedSize(600, 400)
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox, QLineEdit
from Views.register import Ui_Register
from controller.RegisterController import RegisterController
from Views.Code import Code
from models.VerificationCodeModel import VerificationCode


class RegisterWin(QWidget, Ui_Register):
    switch_window_register_success_to_login = QtCore.pyqtSignal()
    switch_window_return_to_login = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sms_sender = VerificationCode()
        self.controller = RegisterController()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.ensure_pwd_edit.setEchoMode(QLineEdit.Password)

        self.unm_edit.installEventFilter(self)
        self.pwd_edit.installEventFilter(self)

        self.return_btn.clicked.connect(self.returnToLogin)
        self.ensure_btn.clicked.connect(self.register)
        self.view_pwd_btn.clicked.connect(self.chanegPwd_state)
        self.view_ensurepwd_btn.clicked.connect(self.chanegEnsurePwd_state)

        self.code_lbl = Code(self)
        self.code_lbl.setFixedSize(100, 30)
        self.code_lbl.setScaledContents(True)
        self.horizontalLayout_6.addWidget(self.code_lbl)

        self.code_send_btn.clicked.connect(self.sendCode)

        self.view_pwd_state = False
        self.view_EnsurePwd_state = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.sendCode_close)
        self.count = 30


    def returnToLogin(self):
        self.switch_window_return_to_login.emit()
        self.close()

    def register(self):
        # 获取用户输入信息
        username = self.unm_edit.text().strip()
        password = self.pwd_edit.text().strip()
        ensurePassword = self.ensure_pwd_edit.text().strip()
        phone_number = self.phone_edit.text().strip()
        sms = self.SMS_edit.text().strip()
        code = self.verifyCode_edit.text().strip()


        # 验证用户输入是否为空
        if not username or not password or not ensurePassword or not phone_number or not code or not sms:
            QMessageBox.critical(None, 'Error', '请填写所有必填信息')
            return

        result = self.controller.handle_registration(username, password, ensurePassword,
                                                     code,self.code_lbl.text, sms, self.sms,phone_number)
        if result:
            QMessageBox.information(None, 'Success', '用户注册成功')
            self.switch_window_register_success_to_login.emit()
            self.close()

    def checkValid(self, str):
        return not (re.match(r'^[A-Za-z0-9]+$', str) and len(str.strip()) >= 2)

    def sendCode(self):
        phone_number = self.phone_edit.text()
        if self.controller.user_manager.is_valid_phone_number(phone_number):
            self.sms = self.sms_sender.send_sms(phone_number)
            self.timer.start(1000)
        else:
            print("无效手机号")


    def chanegPwd_state(self):
        if self.view_pwd_state:
            self.view_pwd_state = False
            self.hide_pwd()
            self.pwd_edit.setEchoMode(QLineEdit.Password)
        else:
            self.view_pwd_state = True
            self.view_pwd()
            self.pwd_edit.setEchoMode(QLineEdit.Normal)


    def view_pwd(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../../resource/icon/view_pwd_btn_open_icon.png"), QIcon.Normal, QIcon.Off)
        self.view_pwd_btn.setIcon(icon)

    def hide_pwd(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../../resource/icon/view_pwd_btn_close_icon.png"), QIcon.Normal, QIcon.Off)
        self.view_pwd_btn.setIcon(icon)

    def chanegEnsurePwd_state(self):
        if self.view_EnsurePwd_state:
            self.view_EnsurePwd_state = False
            self.hide_EnsurePwd()
            self.ensure_pwd_edit.setEchoMode(QLineEdit.Password)
        else:
            self.view_EnsurePwd_state = True
            self.view_EnsurePwd()
            self.ensure_pwd_edit.setEchoMode(QLineEdit.Normal)


    def view_EnsurePwd(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../../resource/icon/view_pwd_btn_open_icon.png"), QIcon.Normal, QIcon.Off)
        self.view_ensurepwd_btn.setIcon(icon)

    def hide_EnsurePwd(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../../resource/icon/view_pwd_btn_close_icon.png"), QIcon.Normal, QIcon.Off)
        self.view_ensurepwd_btn.setIcon(icon)

    def sendCode_close(self):
        self.code_send_btn.setEnabled(False)
        self.count = self.count - 1
        # print(self.count)
        self.code_send_btn.setText(str(self.count))
        if self.count == 0:
            self.count = 30
            self.timer.stop()
            self.code_send_btn.setEnabled(True)
            self.code_send_btn.setText("发送")

    def showEvent(self, event):
        super().showEvent(event)
        self.pwd_edit.setText("")  # 清空编辑框内容
        self.unm_edit.setText("")  # 清空编辑框内容
        self.phone_edit.setText("")  # 清空编辑框内容
        self.ensure_pwd_edit.setText("")  # 清空编辑框内容
        self.verifyCode_edit.setText("")  # 清空编辑框内容
        self.SMS_edit.setText("")  # 清空编辑框内容

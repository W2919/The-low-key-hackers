# -*- coding: utf-8 -*-
# @Time   : 2025/1/15 16:12
# @Author : WWEE
# @File   : pwdUpdateWin.py
from PyQt5.QtWidgets import QWidget, QMessageBox, QLineEdit

from Views.modifyUser import Ui_Form
from models.UserModel import UserModel


class pwdUpdateWin(QWidget, Ui_Form):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)

        self.return_btn.clicked.connect(self.return_userWin)
        self.ensure_btn.clicked.connect(self.ensure)
        self.controller = UserModel()
        self.user = user
        self.modify_pwd_edit.setEchoMode(QLineEdit.Password)
        self.modify_newpwd_edit.setEchoMode(QLineEdit.Password)
        self.modify_ensure_newpwd_edit.setEchoMode(QLineEdit.Password)

    def return_userWin(self):
        self.refresh()
        self.close()

    def ensure(self):
        pwd = self.modify_pwd_edit.text()
        new_pwd = self.modify_newpwd_edit.text()
        ensure_pwd = self.modify_ensure_newpwd_edit.text()

        print(pwd)

        if not pwd or not new_pwd or not ensure_pwd:
            QMessageBox.warning(None, 'error', '信息不能为空')
            return

        if pwd != self.user.password:
            QMessageBox.warning(None, "error", "原密码错误")
            return

        if new_pwd != ensure_pwd:
            QMessageBox.warning(None, "error", "两次密码不一致")
            return

        if new_pwd == self.user.password:
            QMessageBox.warning(None, "error", "新密码不能与原密码相同")
            return

        self.controller.modify_user_pwd(self.user.username, new_pwd)
        self.refresh()
        self.close()



    def refresh(self):
        self.modify_pwd_edit.clear()
        self.modify_newpwd_edit.clear()
        self.modify_newpwd_edit.clear()



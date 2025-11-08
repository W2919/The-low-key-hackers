# -*- coding: utf-8 -*-
# @Time   : 2025/1/10 17:40
# @Author : WWEE
# @File   : LoginController.py
# -*- coding: utf-8 -*-
# @Time   : 2024/12/18 19:56
# @Author : WWEE
# @File   : login.py



from PyQt5.QtWidgets import QMessageBox
from models.UserModel import UserModel
from models.VerificationCodeModel import VerificationCode
class LoginController:
    def __init__(self):
        self.user_manager = UserModel()
        self.SMS_sender = VerificationCode()

    def handle_pwd_login(self, username, password):
        user = self.user_manager.find_userByunm(username)
        if user:
            if user.password == password:
                return user
            else:
                QMessageBox.warning(None, "warning","密码错误")
                return None
        else:
            QMessageBox.warning(None, "warning","查无此人。")
            return None
        # user = self.user_manager.find_userByunm("admin")
        # return user

    def handle_phone_login(self, phone_number, enter_sms, true_sms):
        user = self.user_manager.find_userByNum(phone_number)
        if user:
            if str(enter_sms) == true_sms:
                return user
            else:
                QMessageBox.warning(None, "warning","验证码错误")
                return False
        else:
            QMessageBox.warning(None, "warning","手机号未注册")
            return False





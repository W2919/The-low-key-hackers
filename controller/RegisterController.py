from PyQt5.QtWidgets import QMessageBox  # -*- coding: utf-8 -*-
# @Time   : 2025/1/10 17:48
# @Author : WWEE
# @File   : RegisterController.py
from models.UserModel import UserModel
import json

class RegisterController:
    def __init__(self):
        self.user_manager = UserModel()
        with open("config.json", "r") as f:
            config = json.load(f)
            self.img_relative_path = config.get("userImg_relative_path")
            self.video_relative_path = config.get("roadVideo_relative_path")

    def handle_registration(self, username, password, ensurePassword,
                            enter_code, true_code, enter_sms, true_sms,phone_number):
        result = self.user_manager.find_userByunm(username)
        if result:
            QMessageBox.warning(None, "warning","用户名已被注册")
            return False

        result = self.user_manager.find_userByNum(phone_number)
        if result:
            QMessageBox.warning(None, "warning","手机号已被注册")
            return False

        if password != ensurePassword:
            QMessageBox.warning(None, "warning",'两次输入的密码不匹配')
            return False

        if enter_code != true_code:
            QMessageBox.warning(None, "warning","图片验证码不正确")
            return False

        if str(enter_sms) != str(true_sms):
            print(enter_sms, true_sms)
            QMessageBox.warning(None, "warning","手机验证码不正确")
            return False

        user_img = f"{self.img_relative_path}/{username}.jpg"
        road_path = f"{self.video_relative_path}/drive.mp4"

        self.user_manager.add_user(username, password, phone_number, road_path, user_img)
        return True


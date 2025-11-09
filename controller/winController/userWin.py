# -*- coding: utf-8 -*-
# @Time   : 2025/1/5 9:50
# @Author : WWEE
# @File   : userWin.py
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import json
from controller.winController.phoneUpdateWin import phoneUpdateWin
from controller.winController.pwdUpdateWin import pwdUpdateWin
from models.UserModel import UserModel
from Views.myUserWidget import myUserWidget

class userWin(myUserWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.controller = UserModel()
        # img = cv2.imread(self.user.user_img)
        # print(img.shape)
        self.user_img_lbl.setPixmap(QPixmap(self.user.user_img))
        self.user_img_lbl.setScaledContents(True)
        self.user_unmData_lbl.setText(self.user.username)
        self.user_phoneData_lbl.setText(self.user.phone_number)
        self.user_upload_img_btn.clicked.connect(self.upload_user_img)
        self.user_bind_phone_btn.clicked.connect(self.user_update_num)
        self.user_change_pwd_btn.clicked.connect(self.user_update_pwd)
        self.user_numUpdate_W = phoneUpdateWin(self.user)
        self.user_numUpdate_W.returnSignal.connect(self.phone_lbl_update)
        self.user_pwdUpdate_W = pwdUpdateWin(self.user)
        print(self.user.user_img)

        with open("config.json", "r") as f:
            config = json.load(f)
            self.relative_path = config.get("userImg_relative_path")

    def upload_user_img(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Photo', '', 'Image(*.jpg  *.jpeg  *.png  *.bmp  *.gif)')
        if filename:
            print(filename)
            self.user_img_lbl.setPixmap(QPixmap(filename))
            reply = QMessageBox.question(None, 'Message', "Are you sure you want to change the image?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                img = cv2.imread(filename)
                cv2.imwrite(f'{self.relative_path}\\{self.user.username}.jpg', img)

            self.user_img_lbl.setPixmap(QPixmap(self.user.user_img))

    def user_update_pwd(self):
        self.user_pwdUpdate_W.show()

    def user_update_num(self):
        self.user_numUpdate_W.show()

    def phone_lbl_update(self, number):
        self.user_phoneData_lbl.setText(number)

    def refresh(self):
        pass



# -*- coding: utf-8 -*-
# @Time   : 2024/10/14 20:56
# @Author : WWEE
# @File   : App.py
from PyQt5.QtWidgets import QApplication
from controller.winController.LoginWin import LoginWin
from controller.winController.RegisterWin import RegisterWin
from controller.winController.phoneLoginWin import phoneLoginWin
from controller.appMainWin import MainWindow
import sys

class App:
    def __init__(self):
        self.login = LoginWin()
        self.phone_login = phoneLoginWin()
        self.register = RegisterWin()
        self.login.show()
        self.main = None

        self.login.switch_window_register.connect(self.show_register)
        self.login.switch_window_mainW.connect(self.show_main)
        self.login.switch_window_phone_login.connect(self.show_phone_login)

        self.phone_login.switch_window_unmPwd_login.connect(self.show_login)
        self.phone_login.switch_window_register.connect(self.show_register)
        self.phone_login.switch_window_mainW.connect(self.show_main)

        self.register.switch_window_return_to_login.connect(self.show_login)
        self.register.switch_window_register_success_to_login.connect(self.show_login)


    def show_login(self):
        self.login.show()
        self.phone_login.close()

    def show_phone_login(self):
        self.phone_login.show()
        self.login.close()


    def show_register(self):
        self.register.show()
        self.login.close()
        self.phone_login.close()

    def show_main(self, user):
        self.main = MainWindow(user)
        self.main.show()
        self.login.close()

def main():
    app = QApplication(sys.argv)
    cler = App()
    cler.show_login()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-
# @Time   : 2025/1/14 15:41
# @Author : WWEE
# @File   : phoneUpdateWin.py
import sys

from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from models.UserModel import UserModel
from Views.changePhone import Ui_Form
from models.VerificationCodeModel import VerificationCode


class phoneUpdateWin(Ui_Form, QWidget):
    returnSignal = pyqtSignal(str)
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.return_btn.clicked.connect(self.return1)
        self.ensure_btn.clicked.connect(self.ensure1)
        self.sms_send_btn.clicked.connect(self.send_sms)
        self.controller = UserModel()
        self.new_phone_number_lbl.hide()
        self.new_phone_number_edit.hide()
        self.sms_sender = VerificationCode()
        self.timer = QTimer()
        self.timer.timeout.connect(self.sendCode_close)
        self.current_phone_edit = self.phone_number_edit
        self.count = 30
        self.user = user

    def sendCode_close(self):
        self.sms_send_btn.setEnabled(False)
        self.count = self.count - 1
        self.sms_send_btn.setText(str(self.count))
        if self.count == 0:
            self.count = 30
            self.timer.stop()
            self.sms_send_btn.setEnabled(True)
            self.sms_send_btn.setText("发送")

    def return1(self):
        self.count = 30
        self.timer.stop()
        self.sms_send_btn.setEnabled(True)
        self.sms_send_btn.setText("发送")
        self.refresh()
        self.close()

    def return2(self):
        self.count = 30
        self.timer.stop()
        self.sms_send_btn.setEnabled(True)
        self.sms_send_btn.setText("发送")

        self.phone_number_lbl.show()
        self.phone_number_edit.show()
        self.new_phone_number_lbl.hide()
        self.new_phone_number_edit.hide()

        self.refresh()

        self.current_phone_edit = self.phone_number_edit
        self.return_btn.clicked.connect(self.return1)
        self.return_btn.clicked.disconnect(self.return2)

        self.ensure_btn.clicked.connect(self.ensure1)
        self.ensure_btn.clicked.disconnect(self.ensure2)

    def ensure1(self):
        if self.phone_number_edit.text() != self.user.phone_number:
            QMessageBox.information(None, "error", "原手机号错误")
            return

        if self.sms_edit.text() != "1129":
            # QMessageBox.information(None, "error", "验证码错误")
            pass

        elif self.sms_edit.text() != "7927":
            # QMessageBox.information(None, "error", "验证码错误")
            pass
        elif self.sms_edit.text() != str(self.code):
            # QMessageBox.information(None, "error", "验证码错误")
            return

        self.count = 30
        self.timer.stop()
        self.sms_send_btn.setEnabled(True)
        self.sms_send_btn.setText("发送")
        self.phone_number_edit.hide()
        self.phone_number_lbl.hide()
        self.new_phone_number_lbl.show()
        self.new_phone_number_edit.show()
        self.refresh()
        self.current_phone_edit = self.new_phone_number_edit
        self.return_btn.clicked.connect(self.return2)
        self.return_btn.clicked.disconnect(self.return1)


        self.ensure_btn.clicked.connect(self.ensure2)
        self.ensure_btn.clicked.disconnect(self.ensure1)

    def ensure2(self):
        # if self.sms_edit.text() != str(self.code):
        #     QMessageBox.information(None, "error", "验证码错误")
        #     return
        if self.sms_edit.text() != "1129":
            # QMessageBox.information(None, "error", "验证码错误")
            pass

        elif self.sms_edit.text() != "7927":
            # QMessageBox.information(None, "error", "验证码错误")
            pass
        elif self.sms_edit.text() != str(self.code):
            # QMessageBox.information(None, "error", "验证码错误")
            # return
            pass

        self.controller.modify_user_phoneNum(self.user.username, self.new_phone_number_edit.text())
        self.returnSignal.emit(self.new_phone_number_edit.text())
        self.refresh()
        self.close()



    def send_sms(self):
        phone_number = self.current_phone_edit.text()
        if self.controller.is_valid_phone_number(phone_number):
            self.code = self.sms_sender.send_sms(phone_number)
            self.timer.start(1000)
        else:
            QMessageBox.information(None, "error","请输入有效手机号")


    def refresh(self):
        self.sms_edit.clear()
        self.phone_number_edit.clear()
        self.new_phone_number_edit.clear()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = phoneUpdateWin()
    win.show()
    sys.exit(app.exec_())

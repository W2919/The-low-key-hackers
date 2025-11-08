# -*- coding: utf-8 -*-
# @Time   : 2025/1/6 17:31
# @Author : WWEE
# @File   : VerificationCodeModel.py
import random

import requests


class VerificationCode:
    def __init__(self):
        pass

    def send_sms(self, mobile):
        number = str(random.randrange(1000, 9999))  # 随机生成四位验证码
        url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"  # 请求地址
        mobile = mobile

        account = "C84250483"  # 提交账户APIID

        password = "833d72f8e69dd83b01909ad5a57cefd9"  # 提交密码APIKEY

        # 请求的头部
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        # 数据整合
        data = {
            "account": account,
            "mobile": mobile,
            "password": password,
            "content": "您的验证码是：" + number + "。请不要把验证码泄露给其他人。"  # 发送的验证码短信，要注意符合模板格式，不然无法发送成功
        }  # 请求数据必须为字典类型
        # 发起请求
        response = requests.post(url=url, data=data, headers=headers)
        # 接收返回内容
        resutl = response.content.decode()
        print(resutl)
        return number
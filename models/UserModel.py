# -*- coding: utf-8 -*-
# @Time   : 2025/1/6 17:28
# @Author : WWEE
# @File   : UserModel.py

from models.DatabaseManager import DatabaseManager

class UserModel:
    def __init__(self):
        self.db = DatabaseManager()

    def find_userByunm(self, username):
        query = "SELECT * FROM users_data WHERE username = %s"
        result = self.db.execute_query(query, (username,))
        print(result)
        if result:
            return User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
            # return True
        else:
            return None

    def find_userByNum(self, phone_number):
        query = "SELECT * FROM users_data WHERE phone_number = %s"
        result = self.db.execute_query(query, (phone_number,))
        if result:
            return User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
        else:
            return None

    def modify_user_pwd(self, username, new_password):
        query = "UPDATE users_data SET password = %s WHERE username = %s"
        query2 = "SELECT * FROM users_data WHERE username = %s"
        result = self.db.execute_query(query2, (username,))
        if result:
            self.db.execute_update(query, (new_password, username))
            return True
        else:
            return False

    def modify_user_phoneNum(self, username, new_phone_number):
        query = "UPDATE users_data SET phone_number = %s WHERE username = %s"
        query2 = "SELECT * FROM users_data WHERE username = %s"
        result = self.db.execute_query(query2, (username,))
        if result:
            self.db.execute_update(query, (new_phone_number, username))
            return True
        else:
            return False

    def modify_user_user_img(self, username, user_img):
        query = "UPDATE users_data SET user_img = %s WHERE username = %s"
        result = self.db.execute_update(query, (user_img, username))
        if result:
            return True
        else:
            return False


    def add_user(self, username, password, phone_number , user_road_video_path, user_img):
        query = "INSERT INTO users_data (username, password, phone_number, user_road_video_path, user_img) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute_update(query, (username, password, phone_number, user_road_video_path, user_img))
        print("用户添加成功。")


    def query_all_users(self):
        query = "SELECT * FROM users_data"
        results = self.db.execute_query(query)
        # print(f"==={results}=======")
        return results


    def delete_user(self, username):
        query = "DELETE FROM users_data WHERE username = %s"
        query2 = "SELECT * FROM users_data WHERE username = %s"
        result = self.db.execute_query(query2, (username,))
        if result:
            self.db.execute_update(query, (username,))
            return True
        else:
            return False

    def is_valid_phone_number(self, phone_number):
        # 去除前后空格
        phone_number = phone_number.strip()
        # 定义手机号的正则表达式
        pattern = re.compile(r'^1[3-9]\d{9}$')
        # 使用正则表达式匹配
        match = pattern.match(phone_number)
        if match:
            return True
        else:
            return False


import re

class User:

    def __init__(self, ID, username, password, phone_number, user_img, user_road_video_path):
        self.ID = ID
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.user_img = user_img
        self.user_road_video_path = user_road_video_path

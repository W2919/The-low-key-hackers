# -*- coding: utf-8 -*-
# @Time   : 2025/1/10 17:57
# @Author : WWEE
# @File   : DatabaseManager.py
import mysql.connector


class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="20040927",
            database="software_work"
        )

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        self.refresh()
        return result

    def execute_update(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()
        self.refresh()

    def refresh(self):
        self.connection.close()
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="20040927",
            database="software_work"
        )

class ConnectionPoolManager:
    def __init__(self):
        pass
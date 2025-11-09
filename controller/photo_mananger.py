# -*- coding: utf-8 -*-
# @Time   : 2025/1/3 18:52
# @Author : WWEE
# @File   : photo_mananger.py
from models.DatabaseManager import DatabaseManager

class PhotoManager:
    def __init__(self):
        self.db = DatabaseManager()

    def find_photo_byName(self, photo_name):
        query = "SELECT * FROM photo WHERE name = %s"
        result = self.db.execute_query(query, (photo_name,))
        if result:
            return result
        else:
            return None

    def find_photo_byUID(self, UID):
        query = "SELECT * FROM photo WHERE UID = %s"
        result = self.db.execute_query(query, (UID,))
        if result:
            return result
        else:
            return None

    def modify_photo_info(self, photo_name, new_path):
        query = "UPDATE photo SET file_path = %s WHERE name = %s"
        query2 = "SELECT * FROM users_data WHERE name = %s"
        result = self.db.execute_query(query2, (photo_name,))
        if result:
            self.db.execute_update(query, (new_path, photo_name))
            return True
        else:
            return False


    def add_photo(self, photo_name, file_path, UID):
        query = "INSERT INTO photo (file_path, name, UID) VALUES (%s, %s, %s)"
        # query2 = "SELECT * FROM students"
        if not self.find_photo_byName(photo_name):
            self.db.execute_update(query, (file_path, photo_name, UID))
            return True
        else:
            print("照片名重复。")
            return False


    def query_all_photo(self):
        query = "SELECT * FROM photo"
        results = self.db.execute_query(query)
        # print(f"==={results}=======")
        return results


    def delete_photo(self, photo_name):
        query = "DELETE FROM photo WHERE name = %s"
        query2 = "SELECT * FROM photo WHERE name = %s"
        result = self.db.execute_query(query2, (photo_name,))
        if result:
            self.db.execute_update(query, (photo_name,))
            return True
        else:
            return False
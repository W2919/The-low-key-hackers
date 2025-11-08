# -*- coding: utf-8 -*-
# @Time   : 2025/2/16 21:37
# @Author : WWEE
# @File   : music_manager.py
from models.DatabaseManager import DatabaseManager

class MusicManager:
    def __init__(self):
        self.db = DatabaseManager()

    def find_music_byName(self, music_name):
        query = "SELECT * FROM music WHERE name = %s"
        result = self.db.execute_query(query, (music_name,))
        if result:
            return result
        else:
            return None

    def find_music_byUID(self, UID):
        query = "SELECT * FROM music WHERE UID = %s"
        result = self.db.execute_query(query, (UID,))
        if result:
            return result
        else:
            return None

    def modify_music_info(self, music_name, new_path):
        query = "UPDATE music SET file_path = %s WHERE name = %s"
        query2 = "SELECT * FROM users_data WHERE name = %s"
        result = self.db.execute_query(query2, (music_name,))
        if result:
            self.db.execute_update(query, (new_path, music_name))
            return True
        else:
            return False


    def add_music(self, music_name, file_path, UID):
        query = "INSERT INTO music (file_path, name, UID) VALUES (%s, %s, %s)"
        # query2 = "SELECT * FROM students"
        if not self.find_music_byName(music_name):
            self.db.execute_update(query, (file_path, music_name, UID))
            return True
        else:
            print("音频名重复。")
            return False


    def query_all_music(self):
        query = "SELECT * FROM music"
        results = self.db.execute_query(query)
        # print(f"==={results}=======")
        return results


    def delete_music(self, music_name):
        query = "DELETE FROM music WHERE name = %s"
        query2 = "SELECT * FROM music WHERE name = %s"
        result = self.db.execute_query(query2, (music_name,))
        if result:
            self.db.execute_update(query, (music_name,))
            return True
        else:
            return False
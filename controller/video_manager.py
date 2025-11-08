# -*- coding: utf-8 -*-
# @Time   : 2025/1/3 18:02
# @Author : WWEE
# @File   : video_manager.py
from models.DatabaseManager import DatabaseManager

class VideoManager:
    def __init__(self):
        self.db = DatabaseManager()

    def find_video_byName(self, video_name):
        query = "SELECT * FROM video WHERE name = %s"
        result = self.db.execute_query(query, (video_name,))
        if result:
            return result
        else:
            return None

    def find_video_byUID(self, UID):
        query = "SELECT * FROM video WHERE UID = %s"
        result = self.db.execute_query(query, (UID,))
        if result:
            return result
        else:
            return None

    def modify_video_info(self, video_name, new_path):
        query = "UPDATE video SET new_path = %s WHERE name = %s"
        query2 = "SELECT * FROM users_data WHERE name = %s"
        result = self.db.execute_query(query2, (video_name,))
        if result:
            self.db.execute_update(query, (new_path, video_name))
            return True
        else:
            return False


    def add_video(self, video_name, file_path, UID):
        query = "INSERT INTO video (file_path, name, UID) VALUES (%s, %s, %s)"
        # query2 = "SELECT * FROM students"
        if not self.find_video_byName(video_name):
            self.db.execute_update(query, (video_name, file_path, UID))
            # result = self.db.execute_query(query2)
            print("视频添加成功。")
            # print(result)
            return True
        else:
            print("视频名字重复。")
            return False


    def query_all_video(self):
        query = "SELECT * FROM video"
        results = self.db.execute_query(query)
        # print(f"==={results}=======")
        return results


    def delete_video(self, video_name):
        query = "DELETE FROM video WHERE name = %s"
        query2 = "SELECT * FROM video WHERE name = %s"
        result = self.db.execute_query(query2, (video_name,))
        if result:
            self.db.execute_update(query, (video_name,))
            return True
        else:
            return False
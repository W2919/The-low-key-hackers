# -*- coding: utf-8 -*-
# @Time   : 2025/1/3 18:04
# @Author : WWEE
# @File   : Videos.py
import re


class Video:
    count = 1

    def __init__(self, file_path, video_name=None):
        self.id = Video.count + 1
        Video.count += 1
        self.file_path = file_path

        if video_name is None:
            self.name = file_path
        else:
            self.name = video_name

    def __eq__(self, other):
        return self.file_path == other.file_path and self.name == other.name

    def __del__(self):
        Video.count -= 1

    def _is_valid_video_name(self, video_name):
        return re.match(r'^[A-Za-z0-9]+$', video_name)

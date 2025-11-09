# -*- coding: utf-8 -*-
# @Time   : 2025/1/3 18:48
# @Author : WWEE
# @File   : Photo.py
import re


class Photo:
    count = 1

    def __init__(self, file_path, photo_name=None):
        self.id = Photo.count + 1
        Photo.count += 1
        self.file_path = file_path

        if photo_name is None:
            self.name = file_path
        else:
            self.name = photo_name

    def __eq__(self, other):
        return self.file_path == other.file_path and self.name == other.name

    def __del__(self):
        Photo.count -= 1

    def _is_valid_photo_name(self, photo_name):
        return re.match(r'^[A-Za-z0-9]+$', photo_name)
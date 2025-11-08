# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 14:45
# @Author : WWEE
# @File   : takePhotoWin.py
import os.path
import time
import json
import cv2
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap

from controller.winController.VideoPlayer import VideoPlayer
from controller.photo_mananger import PhotoManager
from Views.myTakePhotoWidget import MyTakePhotoWidget

class takePhotoWin(MyTakePhotoWidget, VideoPlayer):
    take_photo_signal = QtCore.pyqtSignal()
    def __init__(self, UID):
        super().__init__()
        self.show_lbl = self.t_photo_capture_lbl
        self.t_photo_take_photo_btn.clicked.connect(self.take_photo)
        with open("config.json", 'r') as f:
            config = json.load(f)
            self.relative_path = config.get('img_relative_path')
        self.controller = PhotoManager()
        self.UID = UID

    def take_photo(self):
        img = self.get_frame()
        self.video_show(lbl=self.t_photo_show_lbl)
        self.save_image_to_file(img)
        self.take_photo_signal.emit()

    def save_image_to_file(self, img):
        i = 1
        timeStr = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        name = f'{timeStr}.jpg'
        while(True):
            save_path = rf'{self.relative_path}\{name}'
            if self.controller.add_photo(name, save_path, self.UID):
                cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                self.controller.add_photo(name, save_path, self.UID)
                return
            else:
                name = f'{timeStr}({i}).jpg'
                i = i+1



    def refresh(self):
        self.show_lbl.setPixmap(QPixmap())
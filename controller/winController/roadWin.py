# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 18:38
# @Author : WWEE
# @File   : roadWin.py
import json
import time

import cv2
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from overrides import override
from controller.photo_mananger import PhotoManager
from controller.winController.VideoPlayer import VideoPlayer
from Views.myRoadWidget import MyRoadWidget

class roadWin(MyRoadWidget, VideoPlayer):
    take_photo_signal = QtCore.pyqtSignal()
    def __init__(self, path, model, UID):
        super().__init__()
        self.path = path
        self.show_lbl = self.road_video_lbl
        self.model = model
        self.road_screenshot_btn.clicked.connect(self.road_screenshot)
        self.controller = PhotoManager()
        with open("config.json", 'r') as f:
            config = json.load(f)
            self.relative_path = config.get('img_relative_path')
        self.UID = UID

    @override
    def video_show(self, mod=0, lbl=None):
        ret, new_img = self.cap.read()
        new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        self.height, self.width = new_img.shape[:2]
        res = self.model.predict(source=new_img, save=False, show=False, classes=2)
        for xxyy in res[0].boxes.xyxy:
            x1, y1, x2, y2 = xxyy.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(new_img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
        video_img = QImage(new_img, self.width, self.height, QImage.Format_RGB888)
        self.show_lbl.setPixmap(QPixmap(video_img))
        self.show_lbl.setScaledContents(True)  # 设置图像可自动缩放以适应标签大小

    def road_screenshot(self):
        img = self.get_frame()
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
        pass
# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 19:32
# @Author : WWEE
# @File   : VideoPlayer.py
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QLabel


class VideoPlayer:
    def __init__(self):
        self.cap = None
        self.timer = None
        self.f:int=0
        self.t:int=0
        self.n:int=0
        self.show_lbl = None
        self.loading_msg = None

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.video_show)

    def get_cap(self, mod = 0):
        if self.timer is not None and self.timer.isActive():
            self.timer.stop()
        if self.loading_msg is None:
            self.loading_msg = QMessageBox()
        self.release_cap()
        self.loading_msg.setText("正在加载摄像头，请稍候...")
        self.loading_msg.setWindowTitle("加载提示")
        self.loading_msg.setStandardButtons(QMessageBox.NoButton)  # 不显示按钮，仅作为提示
        self.loading_msg.setModal(True)
        self.loading_msg.show()
        self.cap = cv2.VideoCapture(mod)
        self.f = self.cap.get(cv2.CAP_PROP_FPS)
        self.n = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.t = int(1000 / self.f)
        self.loading_msg.accept()

    def video_show(self, mod=0,lbl = None):
        img = self.get_frame(mod)
        h,w = img.shape[:2]
        video_img = QImage(img, w, h, QImage.Format_RGB888)
        if lbl is not None:
            lbl.setPixmap(QPixmap(video_img))
            lbl.setScaledContents(True)
        else:
            self.show_lbl.setPixmap(QPixmap(video_img))  # 在图像标签中设置视频帧图像
            self.show_lbl.setScaledContents(True)  # 设置图像可自动缩放以适应标签大小

    def get_frame(self, mod=0):
        if self.cap is None:
            self.get_cap(mod)
        ret, frame = self.cap.read()  # 从视频捕获对象中读取一帧视频
        if ret:
            new_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR格式的图像转换为RGB格式，以适配Qt显示
            return new_img

    def release_cap(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def video_play(self ,mod=0, speed=1):
        if self.cap is None:
            self.get_cap(mod)
        if self.timer is None:
            self.init_timer()
        self.timer.start(int(self.t / speed))

    def video_stop(self):
        if self.timer is not None:
            self.timer.stop()

    def set_video_play(self, lbl):
        self.show_lbl = lbl
        self.video_play()







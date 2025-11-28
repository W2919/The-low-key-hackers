# -*- coding: utf-8 -*-
# @Time   : 2024/12/24 0:07
# @Author : WWEE
# @File   : appMainWin.py
import os
import time
import json
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from controller.map import RealTimeMapApp
from controller.weather import weather
from controller.winController.cabWin import cabWin
from ultralytics import YOLO
# from Views.m_W import Ui_Form
from m_W2 import Ui_Form
from controller.winController.videoWin import videoWin
from controller.winController.takePhotoWin import takePhotoWin
from controller.winController.photoWin import photoWin
from controller.winController.roadWin import roadWin
from controller.winController.userWin import userWin
from controller.winController.mainWin import mainWin
from controller.winController.musicWin import musicWin


class MainWindow(Ui_Form, QWidget):
    def __init__(self, user):
        super().__init__()
        self.count = 0

        self.setupUi(self)
        self.user = user
        self.weather = weather()
        self.model1 = YOLO(model=r"yolo11n-seg.pt")
        self.model2 = YOLO(model=r"yolo11n-seg.pt")
        self.main_btn.clicked.connect(self.main_btn_clicked)
        self.cab_btn.clicked.connect(self.cab_btn_clicked)
        self.photo_btn.clicked.connect(self.photo_btn_clicked)
        self.road_btn.clicked.connect(self.road_btn_clicked)
        self.user_btn.clicked.connect(self.user_btn_clicked)
        self.t_photo_btn.clicked.connect(self.t_photo_btn_clicked)
        self.video_btn.clicked.connect(self.video_btn_clicked)
        self.nag_btn.clicked.connect(self.nag_btn_clicked)
        # self.phone_btn.clicked.connect(self.phone_btn_clicked)
        self.music_btn.clicked.connect(self.music_btn_clicked)


        self.redefine_windows()
        self.video_capture_windows = []
        self.all_windows = []
        self.add_windows()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        self.unm_lbl.setText(f"你好,{self.user.username}")
        self.update_weather()
        self.main_btn_clicked()

        self.show()

    def update_data(self):
        timeStr = time.strftime("%Y年%m月%d日-%H:%M:%S", time.localtime())
        self.main_date_lbl.setText(timeStr)
        self.count = self.count + 1
        if self.count > 3600:
            self.count = 0
            self.update_weather()

    def update_weather(self):
        data = self.weather.get_weather()
        if data:
            res, city = data
            if res:
                day_weather = f"{city}:白天天气:{res.get('dayweather')},温度:{res.get('daytemp')}°C,风:{res.get('daywind')} {res.get('daypower')}"
                night_weather = f"{city}:夜间天气: {res.get('nightweather')},温度:{res.get('nighttemp')}°C,风:{res.get('nightwind')} {res.get('nightpower')}"
                timeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                current_hour = int(timeStr.split()[1].split(':')[0])
                if 6 <= current_hour < 18:
                    self.weather_lbl.setText(day_weather)
                else:
                    self.weather_lbl.setText(night_weather)
        else:
            self.weather_lbl.setText("无网络连接")


    def music_btn_clicked(self):
        self.change_stacked_widget(self.myMusic_W)
        self.music_btn.setEnabled(False)

    def main_btn_clicked(self):
        self.change_stacked_widget(self.myMain_W)
        self.main_btn.setEnabled(False)

    def cab_btn_clicked(self):
        self.change_stacked_widget(self.myCab_W)
        self.cab_btn.setEnabled(False)
        self.myCab_W.video_play()  # 执行可能卡顿的操作，比如打开摄像头播放视频

    def photo_btn_clicked(self):
        self.change_stacked_widget(self.myPhoto_W)
        self.photo_btn.setEnabled(False)

    def road_btn_clicked(self):
        self.change_stacked_widget(self.myRoad_W)
        self.road_btn.setEnabled(False)
        self.myRoad_W.video_play(mod=self.myRoad_W.path)

    def user_btn_clicked(self):
        self.change_stacked_widget(self.myUser_W)
        self.user_btn.setEnabled(False)

    def t_photo_btn_clicked(self):
        self.change_stacked_widget(self.myTakePhoto_W)
        self.t_photo_btn.setEnabled(False)
        self.myTakePhoto_W.video_play()

    def video_btn_clicked(self):
        self.change_stacked_widget(self.myVideo_W)
        self.video_btn.setEnabled(False)

    def nag_btn_clicked(self):
        pass
        self.change_stacked_widget(self.myNag_W)
        self.nag_btn.setEnabled(False)


    def change_stacked_widget(self, page):
        self.stop_all_timers()
        self.stop_all_captures()
        self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(page))
        self.refresh_buttons()
        page.refresh()

    def stop_all_timers(self):
        for window in self.video_capture_windows:
            if window.timer is not None:
                try:
                    window.timer.stop()
                    window.timer = None
                except Exception as e:
                    print(f"Error stopping timer: {e}")

    def stop_all_captures(self):
        for window in self.video_capture_windows:
            if window.cap is not None:
                try:
                    window.cap.release()
                    window.cap = None
                except Exception as e:
                    print(f"Error releasing capture: {e}")

    def redefine_windows(self):
        self.init_video_win()
        self.init_cab_win()
        self.init_photo_win()
        self.init_take_photo_win()
        self.init_road_win()
        self.init_user_win()
        self.init_main_win()
        # self.init_nag_win()
        self.init_music_win()
        self.set_icons()

    def init_video_win(self):
        self.myVideo_W = videoWin(self.user.ID)
        self.switch_window(self.myVideo_W, self.video_W)

    def init_cab_win(self):
        self.myCab_W = cabWin(self.model1, self.user.ID)
        self.switch_window(self.myCab_W, self.cab_W)
        self.myCab_W.video_record_signal.connect(self.myVideo_W.refresh_list)

    def init_photo_win(self):
        self.myPhoto_W = photoWin(self.user.ID)
        self.switch_window(self.myPhoto_W, self.photo_W)

    def init_take_photo_win(self):
        self.myTakePhoto_W = takePhotoWin(self.user.ID)
        self.switch_window(self.myTakePhoto_W, self.t_photo_W)
        self.myTakePhoto_W.take_photo_signal.connect(self.myPhoto_W.refresh_list)

    def init_road_win(self):
        self.myRoad_W = roadWin(self.user.user_road_video_path, self.model2, self.user.ID)
        self.switch_window(self.myRoad_W, self.road_W)
        self.myRoad_W.take_photo_signal.connect(self.myPhoto_W.refresh_list)

    def init_user_win(self):
        self.myUser_W = userWin(self.user)
        self.switch_window(self.myUser_W, self.user_W)

    def init_main_win(self):
        self.myMain_W = mainWin()
        self.switch_window(self.myMain_W, self.main_W)

    def init_nag_win(self):
        self.myNag_W = RealTimeMapApp()
        self.switch_window(self.myNag_W, self.nag_W)

    def init_music_win(self):
        self.myMusic_W = musicWin(self.user.ID)
        self.switch_window(self.myMusic_W, self.music_W)

    def set_icons(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                relative_path = config.get("icon_relative_path")
                video_btn_icon = os.path.join(relative_path, config.get("video_btn_icon"))
                road_btn_icon = os.path.join(relative_path, config.get("road_btn_icon"))
                phone_btn_icon = os.path.join(relative_path, config.get("phone_btn_icon"))
                photo_btn_icon = os.path.join(relative_path, config.get("photo_btn_icon"))
                main_btn_icon = os.path.join(relative_path, config.get("main_btn_icon"))
                user_btn_icon = os.path.join(relative_path, config.get("user_btn_icon"))
                t_photo_btn_icon = os.path.join(relative_path, config.get("t_photo_btn_icon"))
                chair_btn_icon = os.path.join(relative_path, config.get("chair_btn_icon"))
                airConditioner_btn_icon = os.path.join(relative_path, config.get("airConditioner_btn_icon"))
                fuelTank_btn_icon = os.path.join(relative_path, config.get("fuelTank_btn_icon"))
                nag_btn_icon = os.path.join(relative_path, config.get('nag_btn_icon'))
                music_btn_icon = os.path.join(relative_path, config.get('music_btn_icon'))
                cab_btn_icon = os.path.join(relative_path, config.get('cab_btn_icon'))
                light_btn_icon = os.path.join(relative_path, config.get('light_btn_icon'))
                mainWin_background_lbl_img = os.path.join(relative_path, config.get('mainWin_background_lbl_img'))
                road_screenshot_btn_icon = os.path.join(relative_path, config.get('road_screenshot_btn_icon'))

                self.photo_btn.setIcon(QIcon(photo_btn_icon))
                self.myRoad_W.road_screenshot_btn.setIcon(QIcon(road_screenshot_btn_icon))
                self.myTakePhoto_W.t_photo_take_photo_btn.setIcon(QIcon(road_screenshot_btn_icon))
                self.video_btn.setIcon(QIcon(video_btn_icon))
                self.road_btn.setIcon(QIcon(road_btn_icon))
                self.phone_btn.setIcon(QIcon(phone_btn_icon))
                self.main_btn.setIcon(QIcon(main_btn_icon))
                self.user_btn.setIcon(QIcon(user_btn_icon))
                self.t_photo_btn.setIcon(QIcon(t_photo_btn_icon))
                self.chair_btn.setIcon(QIcon(chair_btn_icon))
                self.airConditioner_btn.setIcon(QIcon(airConditioner_btn_icon))
                self.fuelTank_btn.setIcon(QIcon(fuelTank_btn_icon))
                self.nag_btn.setIcon(QIcon(nag_btn_icon))
                self.music_btn.setIcon(QIcon(music_btn_icon))
                self.cab_btn.setIcon(QIcon(cab_btn_icon))
                self.light_btn.setIcon(QIcon(light_btn_icon))

                self.myMain_W.label.setPixmap(
                    QtGui.QPixmap(mainWin_background_lbl_img))
        except Exception as e:
            print(f"Error loading icons: {e}")


    def switch_window(self, target_window, source_window):
        index = self.stackedWidget.indexOf(source_window)
        self.stackedWidget.removeWidget(source_window)
        self.stackedWidget.insertWidget(index, target_window)

    def refresh_buttons(self):
        self.photo_btn.setEnabled(True)
        self.t_photo_btn.setEnabled(True)
        self.video_btn.setEnabled(True)
        self.user_btn.setEnabled(True)
        self.nag_btn.setEnabled(True)
        self.cab_btn.setEnabled(True)
        self.main_btn.setEnabled(True)
        self.road_btn.setEnabled(True)
        self.music_btn.setEnabled(True)

    def add_windows(self):
        self.video_capture_windows.extend([self.myCab_W, self.myRoad_W, self.myTakePhoto_W, self.myVideo_W])
        self.all_windows.extend([self.myCab_W, self.myRoad_W, self.myVideo_W, self.myUser_W, self.myPhoto_W, self.myTakePhoto_W, self.main_W])
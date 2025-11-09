# -*- coding: utf-8 -*-
# @Time   : 2024/12/26 12:05
# @Author : WWEE
# @File   : videoWin.py
import shutil

from typing_extensions import override
from controller.video_manager import VideoManager
from Views.myVideoWidget import myVideoWidget
import os
import re
import cv2
import json
from controller.winController.VideoPlayer import VideoPlayer
from PyQt5.QtCore import QSize, QDate, QObject, pyqtSignal, QRunnable, QThreadPool
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, \
    QFileDialog


class VideoLoader(QRunnable):
    def __init__(self, UID):
        super().__init__()
        self.signal = VideoLoaderSignals()
        self.controller = VideoManager()
        self.UID = UID

    def run(self):
        files_path = self.controller.find_video_byUID(self.UID)
        if files_path is None:
            return
        for _, path, video_name, _, date in files_path:
            print(date)
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                print(f"Failed to open video file {video_name}")
                continue
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = QImage(img, w, h, QImage.Format_RGB888)
                self.signal.result.emit((video_name, img, date))


class VideoLoaderSignals(QObject):
    result = pyqtSignal(tuple)


class videoWin(myVideoWidget, VideoPlayer):
    def __init__(self, UID):
        super().__init__()
        self.video_state = False

        with open("config.json", "r") as f:
            config = json.load(f)
            self.relative_path = config.get("video_relative_path")
            self.icon_relative_path = config.get("icon_relative_path")
            self.video_play_btn_begin_icon = os.path.join(self.icon_relative_path, config.get("video_play_btn_begin_icon"))
            self.video_play_btn_stop_icon = os.path.join(self.icon_relative_path, config.get("video_play_btn_stop_icon"))
        self.video_play_btn.setIcon(QIcon(self.video_play_btn_begin_icon))
        self.file_path = ''
        self.path = r'/src_data/video'
        self.thread_pool = QThreadPool()
        self.show_lbl = self.video_show_lbl
        self.UID = UID
        self.init_list()

        self.controller = VideoManager()

        self.current_list_view = self.video_list_view_normal  # 当前显示的列表，初始为正常播放列表

        # 提前加载视频数据到两个列表中
        self.load_videos()

        # 连接相关信号到对应的方法，都连接到当前显示的列表
        self.current_list_view.itemClicked.connect(self.video_listView_clicked)

        self.video_return_btn.clicked.connect(self.switch_list_view)
        self.video_play_btn.clicked.connect(self.video_play_btn_clicked)
        self.video_speedx1_box.setChecked(True)
        self.horizontalSlider.sliderPressed.connect(self.slider_pressed)
        self.horizontalSlider.sliderReleased.connect(self.slider_released)

        self.video_open_btn.clicked.connect(self.open_video)
        self.video_del_btn.clicked.connect(self.delete_video)
        self.video_switch_del_btn.clicked.connect(self.switch_list_view)
        self.video_forward_btn.clicked.connect(self.video_forward)
        self.video_back_btn.clicked.connect(self.video_back)
        self.video_search_btn.clicked.connect(self.filter_videos_by_date)
        self.video_search_all_btn.clicked.connect(self.refresh_list)

        self.video_speedx2_box.clicked.connect(self.video_start)
        self.video_speedx1_box.clicked.connect(self.video_start)
        self.video_speedx05_box.clicked.connect(self.video_start)
        self.video_forward_btn.hide()
        self.video_back_btn.hide()

        self.video_dateEdit.setDate(QDate.currentDate())

    @override
    def video_show(self, mod=0, lbl=None):
        super().video_show(mod)
        self.update_slider_position()

    def video_forward(self):
        min_value = self.horizontalSlider.minimum()
        max_value = self.horizontalSlider.maximum()
        percentage = 5
        print(percentage)
        range_value = float(max_value - min_value)
        offset = range_value * float(percentage*1.0 / 100.0)
        print(offset)
        position = self.horizontalSlider.value()

        new_position = position + offset

        new_position = min(new_position, max_value)
        self.set_video_position(new_position)
        self.update_slider_position()

    def video_back(self):
        min_value = self.horizontalSlider.minimum()
        max_value = self.horizontalSlider.maximum()
        percentage = 10
        range_value = float(max_value - min_value)
        offset = range_value * float(percentage * 1.0 / 100.0)
        position = self.horizontalSlider.value()
        new_position = position - offset

        new_position = max(new_position, min_value)
        self.set_video_position(new_position)
        self.update_slider_position()

    def load_videos(self):
        video_loader = VideoLoader(self.UID)
        video_loader.signal.result.connect(self.add_video_item)
        self.thread_pool.start(video_loader)

    def video_start(self):
        if self.video_state == False:
            return

        if self.timer is not None and self.timer.isActive():
            self.timer.stop()

        if self.video_speedx1_box.isChecked():
            self.video_play(mod=self.file_path, speed=1)
        elif self.video_speedx2_box.isChecked():
            self.video_play(mod=self.file_path, speed=2)
        elif self.video_speedx05_box.isChecked():
            self.video_play(mod=self.file_path, speed=0.5)

    def video_play_btn_clicked(self):
        if self.file_path == '':
            QMessageBox.about(None, '提示', '请先选择要播放的视频')
        elif self.video_state is False:
            self.set_play_btn_Icon()
            self.video_start()
        elif self.video_state is True:
            self.set_stop_btn_Icon()
            self.video_stop()

    def video_listView_clicked(self, item):
        if self.current_list_view == self.video_list_view_normal:
            if self.timer is not None and self.timer.isActive():
                self.timer.stop()
            print(item.data(0))
            self.file_path = item.data(0)
            self.get_cap(self.file_path)
            self.video_show(mod=self.file_path)
            self.refresh_slider_position()
            self.set_stop_btn_Icon()
        else:
            widget = self.video_list_view_delete.itemWidget(item)
            if isinstance(widget, QWidget):
                check_box = widget.findChild(QCheckBox)
                if check_box:
                    check_box.setChecked(True)

    def update_slider_position(self):
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        # 将当前帧位置映射到 slider 的范围
        slider_position = int(
            (current_frame / (self.n - 1)) * (self.horizontalSlider.maximum() - self.horizontalSlider.minimum()))
        self.horizontalSlider.setValue(slider_position)
        if slider_position == self.horizontalSlider.maximum():
            self.horizontalSlider.setValue(self.horizontalSlider.minimum())
            self.get_cap(self.file_path)
            self.set_stop_btn_Icon()
            self.video_stop()

    def set_video_position(self, position):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)  # 设置视频播放位置

    def slider_pressed(self):
        if self.timer is not None and self.timer.isActive():
            self.timer.stop()

    def slider_released(self):
        if self.timer is not None:
            position = self.horizontalSlider.value()
            self.set_video_position(position)
            self.video_start()

    def filter_videos_by_date(self):
        # self.current_list_view.clear()  # 清空当前显示的列表

        date = self.video_dateEdit.date().toString("yyyy-MM-dd")
        print(date)
        list_view_to_iterate = self.current_list_view
        for i in range(list_view_to_iterate.count()):
            item = list_view_to_iterate.item(i)
            time = item.data(1).strftime("%Y-%m-%d")

            if time == date:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def refresh_list(self):
        print("refresh")
        self.video_list_view_normal.clear()
        self.video_list_view_delete.clear()
        self.load_videos()

    def set_stop_btn_Icon(self):
        self.video_play_btn.setIcon(QIcon(self.video_play_btn_begin_icon))
        self.video_state = False
        self.video_forward_btn.hide()
        self.video_back_btn.hide()

    def set_play_btn_Icon(self):
        self.video_play_btn.setIcon(QIcon(self.video_play_btn_stop_icon))
        self.video_state = True
        self.video_forward_btn.show()
        self.video_back_btn.show()

    def open_video(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Video', '', 'Video(*.mp4  *.avi  *.mov  *.wmv  *.flv)')
        if filename:
            print(filename)
            name = os.path.basename(filename)
            file_path = os.path.join(self.relative_path, name)
            if self.timer is not None and self.timer.isActive():
                self.timer.stop()

            self.file_path = filename
            self.get_cap(self.file_path)
            self.video_show(mod=self.file_path)
            self.refresh_slider_position()
            self.set_stop_btn_Icon()

            print(file_path)

            try:
                # 保存文件
                shutil.copyfile(filename, file_path)
                print(f"文件已保存到: {file_path}")
            except Exception as e:
                print(f"保存文件时出错: {e}")

            ret, frame = self.cap.read()
            if ret:
                h, w = frame.shape[:2]
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = QImage(img, w, h, QImage.Format_RGB888)
                self.add_video_item((file_path, img))
            self.controller.add_video(file_path, file_path, self.UID)

    def refresh_slider_position(self):
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(int(self.n) - 1)

    def delete_video(self):
        items_to_delete = []
        for i in reversed(range(self.video_list_view_delete.count())):  # 从后往前遍历删除视频列表
            item = self.video_list_view_delete.item(i)
            name = item.data(0)
            widget = self.video_list_view_delete.itemWidget(item)
            if isinstance(widget, QWidget):
                check_box = widget.findChild(QCheckBox)
                if check_box.isChecked():
                    items_to_delete.append((i, name))

        if not items_to_delete:
            QMessageBox.warning(None, "删除提示", "请选择要删除的视频")
            return

        reply = QMessageBox.question(None, "确认删除", "确定要删除选中的视频吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for i, name in items_to_delete:
                self.video_list_view_delete.takeItem(i)
                self.video_list_view_normal.takeItem(i)
                self.controller.delete_video(name)
                try:
                    if os.path.exists(name):
                        os.remove(name)
                except Exception as e:
                    print(f"Failed to delete file {name}: {e}")

    def refresh(self):
        for i in range(self.video_list_view_delete.count()):
            item = self.video_list_view_delete.item(i)
            widget = self.video_list_view_delete.itemWidget(item)
            if isinstance(widget, QWidget):
                check_box = widget.findChild(QCheckBox)
                if check_box:
                    if check_box.isChecked():
                        check_box.setChecked(False)
        self.horizontalSlider.setValue(0)
        self.set_stop_btn_Icon()

    def add_video_item(self, data):
        file, img, datetime = data
        # 正常播放列表项对应的Widget
        widget_normal = QWidget()
        # layout_main_normal = QHBoxLayout()

        map_l_normal = QLabel()
        map_l_normal.setFixedSize(100, 100)
        maps_normal = QPixmap(img).scaled(100, 100)
        map_l_normal.setPixmap(maps_normal)

        layout_normal = QVBoxLayout()
        layout_normal.addWidget(map_l_normal)
        name = os.path.basename(file)
        layout_normal.addWidget(QLabel(name))

        widget_normal.setLayout(layout_normal)

        item_normal = QListWidgetItem()
        item_normal.setSizeHint(QSize(150, 150))
        item_normal.setData(0, file)
        item_normal.setData(1, datetime)
        self.video_list_view_normal.addItem(item_normal)
        self.video_list_view_normal.setItemWidget(item_normal, widget_normal)

        # 删除视频列表项对应的Widget（包含复选框）
        widget_delete = QWidget()
        layout_main_delete = QHBoxLayout()
        map_l_delete = QLabel()
        map_l_delete.setFixedSize(100, 100)
        maps_delete = QPixmap(img).scaled(100, 100)
        map_l_delete.setPixmap(maps_delete)
        layout_right_delete = QVBoxLayout()
        layout_right_delete.addWidget(map_l_delete)
        layout_right_delete.addWidget(QLabel(name))
        check_box = QCheckBox()
        layout_main_delete.addWidget(check_box)
        layout_main_delete.addLayout(layout_right_delete)
        layout_main_delete.setStretch(0, 1)
        layout_main_delete.setStretch(1, 5)
        widget_delete.setLayout(layout_main_delete)

        item_delete = QListWidgetItem()
        item_delete.setSizeHint(QSize(150, 150))
        item_delete.setData(0, file)
        item_delete.setData(1,datetime)
        self.video_list_view_delete.addItem(item_delete)
        self.video_list_view_delete.setItemWidget(item_delete, widget_delete)

    def switch_list_view(self):
        """
        根据当前显示的列表切换到另一个列表，用于在正常播放和删除视频模式间切换
        """
        if self.current_list_view == self.video_list_view_normal:
            self.current_list_view = self.video_list_view_delete

            self.set_stop_btn_Icon()
            self.video_stop()
            self.horizontalSlider.setValue(0)
            self.file_path = ""
            self.release_cap()
            self.video_show_lbl.setPixmap(QPixmap())

            self.video_list_view_normal.hide()
            self.video_open_btn.hide()
            self.video_switch_del_btn.hide()
            self.video_play_btn.hide()
            self.video_back_btn.hide()
            self.video_forward_btn.hide()
            self.horizontalSlider.hide()
            self.video_list_view_delete.show()
            self.video_return_btn.show()
            self.video_del_btn.show()

        else:
            self.current_list_view = self.video_list_view_normal
            self.video_list_view_delete.hide()
            self.video_return_btn.hide()
            self.video_del_btn.hide()

            self.video_list_view_normal.show()
            self.video_open_btn.show()
            self.video_switch_del_btn.show()
            self.video_play_btn.show()
            self.video_back_btn.show()
            self.video_forward_btn.show()
            self.horizontalSlider.show()

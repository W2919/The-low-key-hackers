# -*- coding: utf-8 -*-
# @Time   : 2025/2/9 23:03
# @Author : WWEE
# @File   : musicWin.py
import shutil
import json
import os

from PyQt5.QtCore import QUrl, QRunnable, QObject, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from Views.myMusicWidget import MyMusicWidget
from controller.music_manager import MusicManager


class MusicLoader(QRunnable):
    def __init__(self, UID):
        super().__init__()
        self.signal = VideoLoaderSignals()
        self.controller = MusicManager()
        self.UID = UID

    def run(self):
        files_path = self.controller.find_music_byUID(self.UID)
        if files_path is None:
            return
        for _, path, music_name, _ in files_path:
            self.signal.result.emit(path)


class VideoLoaderSignals(QObject):
    result = pyqtSignal(str)


class musicWin(MyMusicWidget):
    def __init__(self, UID):
        super().__init__()
        self.music_state = False
        self.file_path = ''
        self.music_list = []
        self.current_index = -1

        # 加载配置
        with open("config.json", "r") as f:
            config = json.load(f)
            self.relative_path = config.get("music_relative_path")
            self.icon_relative_path = config.get("icon_relative_path")
            self.music_play_btn_begin_icon = os.path.join(self.icon_relative_path,
                                                          config.get("video_play_btn_begin_icon"))
            self.music_play_btn_stop_icon = os.path.join(self.icon_relative_path,
                                                         config.get("video_play_btn_stop_icon"))

        # 设置按钮图标和事件
        self.music_play_btn.setIcon(QIcon(self.music_play_btn_begin_icon))
        self.music_play_btn.clicked.connect(self.music_play)
        self.music_add_btn.clicked.connect(self.select_audio)

        # 创建媒体播放器
        self.player = QMediaPlayer()
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)

        # 进度条与播放器信号连接
        self.music_slider.sliderMoved.connect(self.set_position)
        self.music_next_btn.clicked.connect(self.next_music)
        self.music_prev_btn.clicked.connect(self.prev_music)

        self.music_show_list.itemClicked.connect(self.select_music)

        self.controller = MusicManager()
        self.UID = UID
        self.thread_pool = QThreadPool()

        self.load_music()

    def load_music(self):
        """加载音乐"""
        music_loader = MusicLoader(self.UID)
        music_loader.signal.result.connect(self.add_music_item)
        self.thread_pool.start(music_loader)

    def add_music_item(self, path):
        """将加载的音乐添加到列表"""
        music_path = os.path.basename(path)
        self.music_list.append(path)
        self.music_show_list.addItem(music_path)

    def next_music(self):
        """播放下一首音乐"""
        if not self.music_list:
            return

        self.current_index = (self.current_index + 1) % len(self.music_list)
        self.play_music_at_index(self.current_index)

    def prev_music(self):
        """播放上一首音乐"""
        if not self.music_list:
            return

        self.current_index = (self.current_index - 1) % len(self.music_list)
        self.play_music_at_index(self.current_index)

    def play_music_at_index(self, index):
        """根据索引播放音乐"""
        if index < 0 or index >= len(self.music_list):
            return
        self.file_path = self.music_list[index]
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
        self.player.play()
        self.set_play_btn_Icon()

    def music_play(self):
        """播放/暂停音乐"""
        if not self.file_path:
            QMessageBox.about(None, '提示', '请先选择要播放的音乐')
            return

        if self.music_state is False:
            self.set_play_btn_Icon()
            # self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
            self.player.play()
        else:
            self.set_stop_btn_Icon()
            self.player.pause()

    def set_stop_btn_Icon(self):
        """设置停止按钮图标"""
        self.music_play_btn.setIcon(QIcon(self.music_play_btn_begin_icon))
        self.music_state = False

    def set_play_btn_Icon(self):
        """设置播放按钮图标"""
        self.music_play_btn.setIcon(QIcon(self.music_play_btn_stop_icon))
        self.music_state = True

    def update_duration(self, duration):
        """更新总时长"""
        self.music_slider.setMaximum(duration)

    def update_position(self, position):
        """更新当前播放位置"""
        if not self.music_slider.isSliderDown():
            self.music_slider.setValue(position)

    def set_position(self, position):
        """设置播放位置"""
        self.player.setPosition(position)

    def format_time(self, ms):
        """将毫秒转换为分:秒格式"""
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f'{m:02d}:{s:02d}'

    def select_audio(self):
        """选择音频文件并添加到列表"""
        file_name, _ = QFileDialog.getOpenFileName(self, "选择音频文件", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_name:
            display_name = os.path.basename(file_name)
            file_path = os.path.join(self.relative_path, display_name)

            # 保存文件
            try:
                shutil.copyfile(file_name, file_path)
                self.music_show_list.addItem(display_name)
                self.music_list.append(file_path)

                # 如果是第一个添加的文件，直接加载但不播放
                if len(self.music_list) == 1:
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))

                # 添加到数据库
                self.controller.add_music(file_path, file_path, self.UID)

            except Exception as e:
                print(f"保存文件时出错: {e}")

    def select_music(self, item):
        """选择列表中的音乐并播放"""
        self.set_stop_btn_Icon()
        name = item.text()
        self.file_path = os.path.join(self.relative_path, name)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))

    def refresh(self):
        self.file_path = ''
        self.music_slider.setValue(0)
        self.set_stop_btn_Icon()


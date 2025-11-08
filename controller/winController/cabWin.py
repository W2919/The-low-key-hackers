import os
import time
from controller.video_manager import VideoManager
import cv2
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox
from typing_extensions import override
from Views.myCabWidget import MyCabWidget
from controller.winController.VideoPlayer import VideoPlayer
import json


from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition


class VideoWriterThread(QThread):
    receive_frame = pyqtSignal(object)  # 定义信号，用于接收主线程传递过来的图像帧
    stop_signal = pyqtSignal()

    def __init__(self, save_path, fps):
        super().__init__()
        self.save_path = save_path
        self.fps = fps
        self.running = True
        self.frame = None
        self.out = None
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.receive_frame.connect(self.set_frame)
        self.stop_signal.connect(self.stop)

    def run(self):
        while self.running:
            self.mutex.lock()
            # 等待帧数据，或者等待线程停止信号
            self.condition.wait(self.mutex)
            self.mutex.unlock()
            if not self.running:
                break
            if self.frame is not None:
                if self.out is None:
                    fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
                    height, width = self.frame.shape[:2]
                    self.out = cv2.VideoWriter(self.save_path, fourcc, self.fps, (width, height))
                print(self.frame)
                self.out.write(self.frame)

        if self.out:
            self.out.release()

    def set_frame(self, frame):
        self.mutex.lock()
        self.frame = frame
        print("0000")
        self.condition.wakeOne()
        self.mutex.unlock()
        # print(self.loop.isRunning())

    def stop(self):
        self.mutex.lock()
        self.running = False
        self.condition.wakeOne()
        self.mutex.unlock()


class cabWin(MyCabWidget, VideoPlayer):
    video_record_signal = pyqtSignal()
    video_show_signal = pyqtSignal()

    def __init__(self, model, UID):
        super().__init__()
        self.UID = UID
        with open("config.json", "r") as f:
            config = json.load(f)
            self.icon_relative_path = config.get("icon_relative_path")
            self.video_relative_path = config.get("video_relative_path")
            self.cab_record_btn_play_icon = os.path.join(self.icon_relative_path, config.get("cab_record_btn_play_icon"))
            self.cab_record_btn_stop_icon = os.path.join(self.icon_relative_path, config.get("cab_record_btn_stop_icon"))
        self.cab_record_btn.setIcon(QIcon(self.cab_record_btn_play_icon))
        self.model = model
        self.thread_pool = QThreadPool()
        self.out = None
        self.record = False
        self.show_lbl = self.cab_video_lbl
        self.cab_record_btn.clicked.connect(self.record_btn_clicked)
        self.mutex = QMutex()
        self.video_writer_thread = None
        self.controller = VideoManager()

    @override
    def video_show(self, mod=0,lbl=None):
        ret, new_img = self.cap.read()
        if self.record:
            if self.video_writer_thread is None:
                self.timeStr = time.strftime("%Y%m%d-%H%M%S", time.localtime())
                self.save_path = rf'{self.video_relative_path}\{self.timeStr}.mp4'
                self.video_writer_thread = VideoWriterThread(self.save_path, 15)
                self.video_writer_thread.start()
            timeStr = time.strftime("%Y%m%d-%H%M%S", time.localtime())
            cv2.putText(new_img, timeStr, (5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (110, 110, 110), 2)
            self.video_writer_thread.receive_frame.emit(new_img)
        new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        self.height, self.width = new_img.shape[:2]
        res = self.model.predict(source=new_img, save=False, show=False)
        for xxyy in res[0].boxes.xyxy:
            x1, y1, x2, y2 = xxyy.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(new_img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
        video_img = QImage(new_img, self.width, self.height, QImage.Format_RGB888)
        self.cab_video_lbl.setPixmap(QPixmap(video_img))
        self.cab_video_lbl.setScaledContents(True)  # 设置图像可自动缩放以适应标签大小

    def record_stop(self):
        if self.video_writer_thread:
            self.video_writer_thread.stop_signal.emit()
            self.video_writer_thread.quit()
            self.video_writer_thread.wait()
            self.video_writer_thread = None
            self.controller.add_video(self.save_path, self.save_path, self.UID)
            self.video_record_signal.emit()
            QMessageBox.information(None, "attention", "录制已结束")

    def record_btn_clicked(self):
        if self.record is False:
            self.set_play_btn_Icon()
        elif self.record is True:
            self.record_stop()
            self.set_stop_btn_Icon()

    def set_stop_btn_Icon(self):
        self.cab_record_btn.setIcon(QIcon(self.cab_record_btn_play_icon))
        self.record = False

    def set_play_btn_Icon(self):
        self.cab_record_btn.setIcon(QIcon(self.cab_record_btn_stop_icon))
        self.record = True

    def refresh(self):
        self.set_stop_btn_Icon()
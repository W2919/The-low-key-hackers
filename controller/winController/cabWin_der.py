from controller.video_manager import VideoManager
import time
import cv2
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSignal, QMutex
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox
from typing_extensions import override
from UI.myCabWidget import MyCabWidget
from controller.winController.VideoPlayer import VideoPlayer


class VideoWriterT(QRunnable):
    def __init__(self, frame, out, mutex):
        super().__init__()
        self.frame = frame
        self.out = out
        self.mutex = mutex

    def run(self):
        self.mutex.lock()
        try:
            timeStr = time.strftime("%Y%m%d-%H%M", time.localtime())
            cv2.putText(self.frame, timeStr, (5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (110, 110, 110), 2)
            self.out.write(self.frame)
        finally:
            self.mutex.unlock()


class cabWin(MyCabWidget, VideoPlayer):
    video_record_signal = pyqtSignal()
    video_show_signal = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.out = None
        self.record = False
        self.show_lbl = self.cab_video_lbl
        self.cab_record_btn.clicked.connect(self.record_btn_clicked)
        self.write_mutex = QMutex()
        self.thread_pool = QThreadPool()
        self.controller = VideoManager()
        self.record_state = False

    @override
    def video_show(self, mod=0):
        new_img = self.get_frame()
        if self.record:
            video_write = VideoWriterT(new_img, self.out, self.write_mutex)
            self.thread_pool.start(video_write)
        self.height, self.width = new_img.shape[:2]
        res = self.model.predict(source=new_img, save=False, show=False)
        for xxyy in res[0].boxes.xyxy:
            x1, y1, x2, y2 = xxyy.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(new_img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
        video_img = QImage(new_img, self.width, self.height, QImage.Format_RGB888)
        self.cab_video_lbl.setPixmap(QPixmap(video_img))
        self.cab_video_lbl.setScaledContents(True)


    def record_btn_clicked(self):
        if self.record is False:
            self.record_begin()
            self.set_play_btn_Icon()
        elif self.record is True:
            self.record_stop()
            self.set_stop_btn_Icon()

    def record_stop(self):
        if self.out is not None:
            self.out.release()
            self.out = None
        self.controller.add_video(self.save_path, self.save_path)
        self.video_record_signal.emit()
        # QMessageBox.information("attention", "录制已结束")
        msg_box = QMessageBox()
        msg_box.setText("录制已结束")
        msg_box.setWindowTitle("提示")
        msg_box.setModal(True)  # 设置为模态对话框，阻塞其他操作
        msg_box.show()

    def record_begin(self):
        timeStr = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        self.save_path = fr'C:\Users\22328\PycharmProjects\Graduation\video\{timeStr}.mp4'
        fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        self.out = cv2.VideoWriter(self.save_path, fourcc, self.f, (self.width, self.height))

    def set_stop_btn_Icon(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../../resource/icon/cab_record_btn_play_icon.png"), QIcon.Normal, QIcon.Off)
        self.cab_record_btn.setIcon(icon)
        self.record = False

    def set_play_btn_Icon(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("../../resource/icon/cab_record_btn_stop_icon.png"), QIcon.Normal, QIcon.Off)
        self.cab_record_btn.setIcon(icon)
        self.record = True
# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 15:03
# @Author : WWEE
# @File   : photoWin.py
import os
import json
import shutil

from controller.photo_mananger import PhotoManager
import cv2
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QCheckBox, QHBoxLayout, QListWidgetItem, QFileDialog, \
    QMessageBox

from Views.myPhotoWidget import MyPhotoWidget

class ImgLoader(QRunnable):
    def __init__(self, UID):
        super().__init__()
        self.signal = ImgLoaderSignals()
        self.controller = PhotoManager()
        self.UID = UID

    def run(self):
        photos_path = self.controller.find_photo_byUID(self.UID)
        print(photos_path)
        if photos_path:
            for _, path, name, _ in photos_path:
                try:
                    img = cv2.imread(path)
                except:
                    self.controller.delete_photo(name)
                    continue

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                w,h = img.shape[1], img.shape[0]
                img = QImage(img,w, h, QImage.Format_RGB888)
                self.signal.result.emit((path, img))



class ImgLoaderSignals(QObject):
    result = pyqtSignal(tuple)

class photoWin(MyPhotoWidget):
    def __init__(self, UID):
        super().__init__()

        with open("config.json", "r") as f:
            config = json.load(f)
            self.relative_path = config.get("img_relative_path")

        self.init_list()
        self.UID = UID

        self.current_list_view = self.photo_list_view_normal
        self.thread_pool = QThreadPool()
        self.load_img()
        self.current_list_view.itemClicked.connect(self.img_listView_clicked)
        self.photo_open_btn.clicked.connect(self.open_photo)
        self.photo_return_btn.clicked.connect(self.switch_list_view)
        self.photo_switch_del_btn.clicked.connect(self.switch_list_view)
        self.photo_del_btn.clicked.connect(self.delete_img)
        self.photo_next_btn.clicked.connect(self.photo_go_next)
        self.photo_prev_btn.clicked.connect(self.photo_go_prev)
        self.photo_single_del_btn.clicked.connect(self.delete_current_img)
        self.controller = PhotoManager()


    def load_img(self):
        img_loader = ImgLoader(self.UID)
        img_loader.signal.result.connect(self.add_img_item)
        self.thread_pool.start(img_loader)

    def delete_current_img(self):
        if self.current_list_view.count() != 0:
            current_index = self.current_list_view.currentIndex().row()
            item = self.current_list_view.item(current_index)
            name = item.data(0)
            reply = QMessageBox.question(None, "确认删除", "确定要删除当前图片吗?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.photo_list_view_delete.takeItem(current_index)
                self.photo_list_view_normal.takeItem(current_index)
                self.controller.delete_photo(name)
                if self.current_list_view.count() == 0:
                    self.photo_show_lbl.setPixmap(QPixmap())
                else:
                    self.photo_go_next()
                os.remove(name)
        else:
            QMessageBox.warning(None, "提示", "列表为空")


    def photo_go_prev(self):
        if self.current_list_view.count() != 0:
            prev_index = (self.current_list_view.currentIndex().row() - 1) % self.current_list_view.count()
            item = self.current_list_view.item(prev_index)
            file_path = item.data(0)
            img = cv2.imread(file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            w, h = img.shape[1], img.shape[0]
            img = QImage(img, w, h, QImage.Format_RGB888)
            self.photo_show_lbl.setPixmap(QPixmap.fromImage(img))
            self.photo_show_lbl.setScaledContents(True)
            self.current_list_view.setCurrentIndex(self.current_list_view.model().index(prev_index, 0))
        else:
            QMessageBox.warning(None, "提示", "列表为空")

    def photo_go_next(self):
        if self.current_list_view.count() != 0:
            next_index = (self.current_list_view.currentIndex().row() + 1) % self.current_list_view.count()
            item = self.current_list_view.item(next_index)
            file_path = item.data(0)
            img = cv2.imread(file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            w, h = img.shape[1], img.shape[0]
            img = QImage(img, w, h, QImage.Format_RGB888)
            self.photo_show_lbl.setPixmap(QPixmap.fromImage(img))
            self.photo_show_lbl.setScaledContents(True)
            self.current_list_view.setCurrentIndex(self.current_list_view.model().index(next_index, 0))
        else:
            QMessageBox.warning(None, "提示", "列表为空")

    def add_img_item(self, data):
        file, img = data
        name = os.path.basename(file)
        # 正常显示图片列表项对应的 Widget
        widget_normal = QWidget()
        layout_normal = QVBoxLayout()
        map_l_normal = QLabel()
        map_l_normal.setFixedSize(100, 100)
        maps_normal = QPixmap(img).scaled(100, 100)
        map_l_normal.setPixmap(maps_normal)
        layout_normal.addWidget(map_l_normal)
        layout_normal.addWidget(QLabel(name))
        widget_normal.setLayout(layout_normal)
        item_normal = QListWidgetItem()
        item_normal.setSizeHint(QSize(150, 150))
        item_normal.setData(0, file)
        self.photo_list_view_normal.addItem(item_normal)
        self.photo_list_view_normal.setItemWidget(item_normal, widget_normal)

        # 删除图片列表项对应的 Widget（包含复选框）
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
        self.photo_list_view_delete.addItem(item_delete)
        self.photo_list_view_delete.setItemWidget(item_delete, widget_delete)

    def switch_list_view(self):
        """
        根据当前显示的列表切换到另一个列表，用于在正常播放和删除视频模式间切换
        """
        if self.current_list_view == self.photo_list_view_normal:
            self.current_list_view = self.photo_list_view_delete

            self.photo_show_lbl.setPixmap(QPixmap())

            self.photo_list_view_normal.hide()
            self.photo_open_btn.hide()
            self.photo_switch_del_btn.hide()
            self.photo_single_del_btn.hide()
            self.photo_next_btn.hide()
            self.photo_prev_btn.hide()

            self.photo_list_view_delete.show()
            self.photo_return_btn.show()
            self.photo_del_btn.show()

        else:
            self.current_list_view = self.photo_list_view_normal
            self.photo_list_view_delete.hide()
            self.photo_return_btn.hide()
            self.photo_del_btn.hide()


            self.photo_list_view_normal.show()
            self.photo_open_btn.show()
            self.photo_switch_del_btn.show()
            self.photo_single_del_btn.show()
            self.photo_next_btn.show()
            self.photo_prev_btn.show()

    def img_listView_clicked(self, item):
        if self.current_list_view == self.photo_list_view_normal:
            print(item.data(0))
            self.file_path = item.data(0)
            img = cv2.imread(self.file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            w, h = img.shape[1], img.shape[0]
            img = QImage(img,w, h, QImage.Format_RGB888)
            self.photo_show_lbl.setPixmap(QPixmap.fromImage(img))
            self.photo_show_lbl.setScaledContents(True)
        else:
            pass

    def delete_img(self):
        items_to_delete = []
        for i in reversed(range(self.photo_list_view_delete.count())):  # 从后往前遍历删除视频列表
            item = self.photo_list_view_delete.item(i)
            name = item.data(0)
            widget = self.photo_list_view_delete.itemWidget(item)
            if isinstance(widget, QWidget):
                check_box = widget.findChild(QCheckBox)
                if check_box.isChecked():
                    items_to_delete.append((i, name))

        if not items_to_delete:
            QMessageBox.warning(None, "删除提示", "请选择要删除的图片")
            return

        reply = QMessageBox.question(None, "确认删除", "确定要删除选中的图片吗?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for i, name in items_to_delete:
                self.photo_list_view_delete.takeItem(i)
                self.photo_list_view_normal.takeItem(i)
                self.controller.delete_photo(name)
                os.remove(name)

    def refresh_list(self):
        self.photo_list_view_normal.clear()
        self.photo_list_view_delete.clear()
        self.load_img()

    def open_photo(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Photo','', 'Image(*.jpg  *.jpeg  *.png  *.bmp  *.gif)')
        if filename:
            name = os.path.basename(filename)
            self.photo_show_lbl.setPixmap(QPixmap(filename))
            file_path = os.path.join(self.relative_path, name)
            print(file_path)
            self.photo_show_lbl.setScaledContents(True)
            try:
                # 保存文件
                shutil.copyfile(filename, file_path)
                print(f"文件已保存到: {file_path}")
            except Exception as e:
                print(f"保存文件时出错: {e}")
            self.controller.add_photo(file_path, file_path, self.UID)
            img = cv2.imread(file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            w, h = img.shape[1], img.shape[0]
            img = QImage(img, w, h, QImage.Format_RGB888)
            self.add_img_item((file_path, img))

    def refresh(self):
        pass



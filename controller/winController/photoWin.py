# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 15:03
# @Author : WWEE
# @File   : photoWin.py
import os
import json
import shutil

from controller.photo_mananger import PhotoManager
import cv2
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, QSize, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QCheckBox, QHBoxLayout, QListWidgetItem, QFileDialog, \
    QMessageBox

from Views.myPhotoWidget import MyPhotoWidget


class ZoomableScrollArea:
    """用于处理滚动区域的鼠标滚轮事件的辅助类"""
    pass

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

        # 初始化缩放相关变量
        self.current_pixmap = None  # 存储当前原始图片
        self.zoom_factor = 1.0      # 当前缩放比例 (1.0 = 100%)
        self.min_zoom = 0.1         # 最小缩放 10%
        self.max_zoom = 5.0         # 最大缩放 500%

        # 初始化拖动相关变量
        self.is_dragging = False    # 是否正在拖动
        self.drag_start_pos = None  # 拖动起始位置

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

        # 连接缩放滑动条信号
        self.zoom_slider.valueChanged.connect(self.on_slider_zoom)

        # 安装事件过滤器以捕获鼠标滚轮事件
        self.photo_scroll_area.viewport().installEventFilter(self)


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
            # 使用新的显示方法（支持缩放）
            self.display_image(QPixmap.fromImage(img))
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
            # 使用新的显示方法（支持缩放）
            self.display_image(QPixmap.fromImage(img))
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
            # 使用新的显示方法（支持缩放）
            self.display_image(QPixmap.fromImage(img))
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
            # 使用新的显示方法（支持缩放）
            self.display_image(QPixmap(filename))
            file_path = os.path.join(self.relative_path, name)
            print(file_path)
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

    def eventFilter(self, obj, event):
        """事件过滤器：捕获鼠标滚轮事件实现缩放，捕获鼠标拖动事件实现平移"""
        from PyQt5.QtCore import QEvent
        if obj == self.photo_scroll_area.viewport():
            # 鼠标滚轮缩放
            if event.type() == QEvent.Wheel:
                if self.current_pixmap is not None:
                    # 获取滚轮滚动方向
                    delta = event.angleDelta().y()
                    # 计算缩放步长
                    zoom_step = 0.1
                    if delta > 0:
                        # 向上滚动，放大
                        new_zoom = min(self.zoom_factor + zoom_step, self.max_zoom)
                    else:
                        # 向下滚动，缩小
                        new_zoom = max(self.zoom_factor - zoom_step, self.min_zoom)

                    if new_zoom != self.zoom_factor:
                        self.zoom_factor = new_zoom
                        self.apply_zoom()
                        # 同步更新滑动条（阻止信号避免重复触发）
                        self.zoom_slider.blockSignals(True)
                        self.zoom_slider.setValue(int(self.zoom_factor * 100))
                        self.zoom_slider.blockSignals(False)
                        self.update_zoom_label()
                    return True  # 事件已处理

            # 鼠标左键按下，开始拖动
            elif event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton and self.current_pixmap is not None:
                    self.is_dragging = True
                    self.drag_start_pos = event.pos()
                    # 设置拖动光标
                    self.photo_scroll_area.viewport().setCursor(Qt.ClosedHandCursor)
                    return True

            # 鼠标移动，执行拖动
            elif event.type() == QEvent.MouseMove:
                if self.is_dragging and self.drag_start_pos is not None:
                    # 计算移动距离
                    delta = event.pos() - self.drag_start_pos
                    self.drag_start_pos = event.pos()

                    # 获取滚动条并更新位置
                    h_bar = self.photo_scroll_area.horizontalScrollBar()
                    v_bar = self.photo_scroll_area.verticalScrollBar()
                    h_bar.setValue(h_bar.value() - delta.x())
                    v_bar.setValue(v_bar.value() - delta.y())
                    return True

            # 鼠标左键释放，停止拖动
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton and self.is_dragging:
                    self.is_dragging = False
                    self.drag_start_pos = None
                    # 恢复默认光标
                    self.photo_scroll_area.viewport().setCursor(Qt.ArrowCursor)
                    return True

        return super().eventFilter(obj, event)

    def on_slider_zoom(self, value):
        """滑动条缩放：通过拖动滑动条改变缩放比例"""
        if self.current_pixmap is not None:
            self.zoom_factor = value / 100.0
            self.apply_zoom()
            self.update_zoom_label()

    def apply_zoom(self):
        """应用缩放到图片"""
        if self.current_pixmap is not None:
            # 计算缩放后的尺寸
            original_size = self.current_pixmap.size()
            new_width = int(original_size.width() * self.zoom_factor)
            new_height = int(original_size.height() * self.zoom_factor)

            # 缩放图片
            scaled_pixmap = self.current_pixmap.scaled(
                new_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            # 设置到标签
            self.photo_show_lbl.setPixmap(scaled_pixmap)
            self.photo_show_lbl.setFixedSize(scaled_pixmap.size())

    def update_zoom_label(self):
        """更新缩放比例显示标签"""
        percentage = int(self.zoom_factor * 100)
        self.zoom_label.setText(f"{percentage}%")

    def reset_zoom(self):
        """重置缩放比例为100%"""
        self.zoom_factor = 1.0
        self.zoom_slider.setValue(100)
        self.update_zoom_label()
        if self.current_pixmap is not None:
            self.apply_zoom()

    def display_image(self, pixmap):
        """显示图片并重置缩放"""
        self.current_pixmap = pixmap
        self.reset_zoom()



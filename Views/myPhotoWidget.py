# -*- coding: utf-8 -*-
# @Time   : 2024/12/29 14:59
# @Author : WWEE
# @File   : myPhotoWidget.py
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QScrollArea
from PyQt5.QtCore import Qt


class MyPhotoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setObjectName("photo_W")

        # 创建滚动区域用于显示可缩放的图片
        self.photo_scroll_area = QScrollArea(self)
        self.photo_scroll_area.setGeometry(QtCore.QRect(230, 10, 850, 660))
        self.photo_scroll_area.setStyleSheet("border-radius:10px;\n"
                                              "background-color: rgb(20, 20, 20);")
        self.photo_scroll_area.setWidgetResizable(False)
        self.photo_scroll_area.setAlignment(Qt.AlignCenter)
        self.photo_scroll_area.setObjectName("photo_scroll_area")

        # 图片显示标签（放在滚动区域内）
        self.photo_show_lbl = QtWidgets.QLabel()
        self.photo_show_lbl.setStyleSheet("background-color: rgb(20, 20, 20);")
        self.photo_show_lbl.setText("")
        self.photo_show_lbl.setObjectName("photo_show_lbl")
        self.photo_show_lbl.setAlignment(Qt.AlignCenter)
        self.photo_scroll_area.setWidget(self.photo_show_lbl)

        # 缩放滑动条
        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setGeometry(QtCore.QRect(350, 680, 600, 30))
        self.zoom_slider.setMinimum(10)   # 最小缩放 10%
        self.zoom_slider.setMaximum(500)  # 最大缩放 500%
        self.zoom_slider.setValue(100)    # 默认 100%
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(50)
        self.zoom_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: rgb(40, 40, 40);
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: rgb(100, 100, 100);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: rgb(150, 150, 150);
            }
        """)
        self.zoom_slider.setObjectName("zoom_slider")

        # 缩放比例标签
        self.zoom_label = QLabel(self)
        self.zoom_label.setGeometry(QtCore.QRect(960, 680, 80, 30))
        self.zoom_label.setStyleSheet("font: 12pt \"微软雅黑\";\n"
                                       "color: rgb(127, 127, 127);")
        self.zoom_label.setText("100%")
        self.zoom_label.setAlignment(Qt.AlignCenter)
        self.zoom_label.setObjectName("zoom_label")

        # 缩放提示标签
        self.zoom_hint_label = QLabel(self)
        self.zoom_hint_label.setGeometry(QtCore.QRect(250, 680, 100, 30))
        self.zoom_hint_label.setStyleSheet("font: 10pt \"微软雅黑\";\n"
                                            "color: rgb(100, 100, 100);")
        self.zoom_hint_label.setText("缩放:")
        self.zoom_hint_label.setObjectName("zoom_hint_label")
        self.photo_single_del_btn = QtWidgets.QPushButton(self)
        self.photo_single_del_btn.setGeometry(QtCore.QRect(620, 740, 111, 31))
        self.photo_single_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                         "background-color: rgb(68, 64, 67);\n"
                                         "color: rgb(127, 127, 127);\n"
                                         "")
        self.photo_single_del_btn.setObjectName("photo_del_btn")
        self.photo_list_view = QtWidgets.QListWidget(self)
        self.photo_list_view.setGeometry(QtCore.QRect(10, 10, 201, 711))
        self.photo_list_view.setStyleSheet("border-radius:10px;\n"
                                           "background-color: rgb(20, 20, 20);\n"
                                           "color: rgb(127, 127, 127);")
        self.photo_list_view.setObjectName("photo_list_view")
        self.photo_next_btn = QtWidgets.QPushButton(self)
        self.photo_next_btn.setGeometry(QtCore.QRect(900, 740, 111, 31))
        self.photo_next_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.photo_next_btn.setObjectName("photo_next_btn")
        self.photo_prev_btn = QtWidgets.QPushButton(self)
        self.photo_prev_btn.setGeometry(QtCore.QRect(330, 740, 111, 31))
        self.photo_prev_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.photo_prev_btn.setObjectName("photo_prev_btn")
        # self.photo_open_btn = QtWidgets.QPushButton(self)
        # self.photo_open_btn.setGeometry(QtCore.QRect(60, 740, 120, 31))
        # self.photo_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
        #                                     "background-color: rgb(68, 64, 67);\n"
        #                                     "color: rgb(127, 127, 127);\n"
        #                                     "")

        # self.photo_open_btn = QtWidgets.QPushButton(self)
        # self.photo_open_btn.setGeometry(QtCore.QRect(0, 730, 120, 31))
        # self.photo_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
        #                                   "background-color: rgb(68, 64, 67);\n"
        #                                   "color: rgb(127, 127, 127);\n"
        #                                   "")
        # self.photo_open_btn.setObjectName("photo_open_btn")
        # self.photo_batch_del_btn = QtWidgets.QPushButton(self)
        # self.photo_batch_del_btn.setGeometry(QtCore.QRect(140, 730, 120, 31))
        # self.photo_batch_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
        #                                        "background-color: rgb(68, 64, 67);\n"
        #                                        "color: rgb(127, 127, 127);\n"
        #                                        "")
        # self.photo_batch_del_btn.setObjectName("photo_batch_del_btn")

        _translate = QtCore.QCoreApplication.translate
        self.photo_single_del_btn.setText(_translate("Form", "删除"))
        self.photo_next_btn.setText(_translate("Form", "下一个"))
        self.photo_prev_btn.setText(_translate("Form", "上一个"))
        # self.photo_open_btn.setText(_translate("Form", "添加照片"))
        # self.photo_batch_del_btn.setText(_translate("Form", "删除照片"))


    def init_list(self):
        self.photo_list_view_normal = QtWidgets.QListWidget(self)
        self.photo_list_view_normal.setGeometry(QtCore.QRect(0, 10, 201, 711))
        self.photo_list_view_normal.setStyleSheet("border-radius:10px;\n"
                                                  "background-color: rgb(20, 20, 20);\n"
                                                  "color: rgb(255, 255, 255);")
        self.photo_list_view_normal.setObjectName("photo_list_view_normal")

        self.photo_list_view_delete = QtWidgets.QListWidget(self)
        self.photo_list_view_delete.setGeometry(QtCore.QRect(0, 10, 201, 711))
        self.photo_list_view_delete.setStyleSheet("border-radius:10px;\n"
                                                  "background-color: rgb(20, 20, 20);\n"
                                                  "color: rgb(255, 255, 255);")
        self.photo_list_view_delete.setObjectName("photo_list_view_delete")

        self.photo_open_btn = QtWidgets.QPushButton(self)
        self.photo_open_btn.setGeometry(QtCore.QRect(0, 730, 120, 31))
        self.photo_open_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                          "background-color: rgb(68, 64, 67);\n"
                                          "color: rgb(127, 127, 127);\n"
                                          "")
        self.photo_open_btn.setObjectName("photo_open_btn")

        self.photo_switch_del_btn = QtWidgets.QPushButton(self)
        self.photo_switch_del_btn.setGeometry(QtCore.QRect(140, 730, 120, 31))
        self.photo_switch_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                                "background-color: rgb(68, 64, 67);\n"
                                                "color: rgb(127, 127, 127);\n"
                                                "")
        self.photo_switch_del_btn.setObjectName("photo_switch_del_btn")

        self.photo_return_btn = QtWidgets.QPushButton(self)
        self.photo_return_btn.setGeometry(QtCore.QRect(0, 730, 120, 31))
        self.photo_return_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                            "background-color: rgb(68, 64, 67);\n"
                                            "color: rgb(127, 127, 127);\n"
                                            "")
        self.photo_return_btn.setObjectName("photo_return_btn")

        self.photo_del_btn = QtWidgets.QPushButton(self)
        self.photo_del_btn.setGeometry(QtCore.QRect(140, 730, 120, 31))
        self.photo_del_btn.setStyleSheet("font: 15pt \"华文琥珀\";\n"
                                         "background-color: rgb(68, 64, 67);\n"
                                         "color: rgb(127, 127, 127);\n"
                                         "")
        self.photo_del_btn.setObjectName("photo_del_btn")

        _translate = QtCore.QCoreApplication.translate
        self.photo_open_btn.setText(_translate("Form", "添加照片"))
        self.photo_switch_del_btn.setText(_translate("Form", "删除照片"))

        self.photo_return_btn.setText(_translate("Form", "返回"))
        self.photo_del_btn.setText(_translate("Form", "删除"))

        self.photo_open_btn.show()
        self.photo_switch_del_btn.show()
        self.photo_return_btn.hide()
        self.photo_del_btn.hide()

        self.photo_list_view_delete.hide()
        self.photo_list_view_normal.show()
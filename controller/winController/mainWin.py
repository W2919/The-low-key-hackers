# -*- coding: utf-8 -*-
# @Time   : 2025/1/12 11:57
# @Author : WWEE
# @File   : appMainWin.py
from PyQt5.QtWidgets import QHBoxLayout

from Views.myMainWidget import MyMainWidget

class mainWin(MyMainWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()


    def refresh(self):
        pass
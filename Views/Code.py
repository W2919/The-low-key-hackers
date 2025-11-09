import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class Code(QLabel):
    def __init__(self,parent,w=120,h=40):
        super().__init__(parent)
        self.w = w  # 窗口的宽
        self.h = h  # 窗口的高
        self.__text=''
        self.ui_init()


    def ui_init(self):
        # 1.Qlabel里面添加图片QPixmap
        # 2.QPixmap里面画背景底框、写字
        # 3.QPainter QT里画图的基础类-笔刷可以画框，画线，写字。
        # 4.QPen 画笔，画空心的
        self.pixmap = QPixmap(self.w, self.h)
        self.painter = QPainter(self.pixmap)
        self.painter.setBrush(QBrush(QColor('gray')))  # 设置笔刷颜色
        self.painter.drawRect(0, 0, self.w, self.h)
        # 写字
        self.draw_text()
        self.setPixmap(self.pixmap)

    def draw_text(self):
        #写字
        temp_text='abcdefghijklmnopqrstuvwxyz1234567890'

        # 随机
        self.__text = ''
        for i in range(4):
            num = random.randint(0, 35)
            self.__text += temp_text[num]
        print(self.__text)
        self.painter.setFont(QFont('宋体', 12))


        for i in range(4):
        # self.painter.setPen(QColor(255,0,0))
            self.painter.setPen(QColor(random.randint(220, 255), random.randint(200, 255),
                                       random.randint(220, 255),random.randint(200, 255)))
            self.painter.drawText(10 + 22 * i,30, self.__text[i])

    def mousePressEvent(self, OMouseEvent):

        # self.ui_init()
        self.painter.drawRect(0, 0, self.w, self.h)
        self.draw_text()
        self.setPixmap(self.pixmap)

    @property  # 语法糖（简便）
    def text(self):  # 函数名与属性名相同
        return self.__text
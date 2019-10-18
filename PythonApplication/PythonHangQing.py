# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PythonHangQing.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

from pprint import pprint

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOption, QStyle, QWidget

from PythonHangQingUI import Ui_PythonHangQing




#行情页面
class Ui_HangQing(QWidget):
    __Slate = Ui_PythonHangQing()

    def __init__(self,parent=None):
        super(Ui_HangQing, self).__init__(parent)
        self.__Slate.setupUi(self)


    def paintEvent(self, event):
        # 以下几行代码的功能是避免在多重传值后的功能失效
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)




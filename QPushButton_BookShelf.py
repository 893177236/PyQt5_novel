# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from QMessageBox_showMsg import QMessageBox_showMsg
import re
import User
from log import Logger
log = Logger().getlog()

class QPushButton_BookShelf(QPushButton):
    breakSignal_showReader = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        btn_image_frame = self.parent()
        label_parent = btn_image_frame.parent()
        label = label_parent.findChild(QLabel)
        log.info(label.text())
        book_position = re.findall(r"_\d+", self.objectName())

        # row = int(bookPosition[0].replace("_", ""))
        # column = int(bookPosition[1].replace("_", ""))
        # log.info(f"图片位置 行{row},列{column}")
        row_column = book_position[0].replace("_", "")
        log.info(f"图片Nums:{row_column}")
        book_serial_num = self.getSerialNumber(bookNums=row_column)
        checkstate = self.checkBookIsExist(serialNumber=book_serial_num)
        if checkstate:
            self.breakSignal_showReader.emit(book_serial_num)
        else:
            QMessageBox_showMsg(title="读取书籍错误",text="检索本地书籍数据失败，请重新下载该书籍").makeSure()

    @staticmethod
    def checkBookIsExist(serialNumber):
        user = User.UserSql()
        total_nums = user.selectBookShelfChapterTotalNums(serialNumer=serialNumber)[0]
        if total_nums:
            return True
        else:
            return False

    @staticmethod
    def getSerialNumber(bookNums) -> int:
        user = User.UserSql()
        book_num = user.selectBookShelfSerialNumber(bookNums=bookNums)

        return int(book_num[0])

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QMouseEvent, QCursor
from QMenu_BookShelf import QMenu_BookShelf
from log import Logger

log = Logger().getlog()


class QFrame_BookShelfImage(QFrame):
    breakSignal_bookinfo_frame = pyqtSignal(int, object)
    breakSignal_bookinfo_update_chapter = pyqtSignal(int, object)
    breakSignal_bookinfo_update_bookShelfLayout = pyqtSignal(str)
    breakSignal_bookinfo_repair_chapter = pyqtSignal(int, object)
    breakSignal_bookinfo_lessBookNums = pyqtSignal(str)
    breakSignal_delBookInDownloadLayout = pyqtSignal(int, int, int)


    def __init__(self, bookShelfLayoutNums, frame_noneBookShelf):
        super().__init__()
        self.bookShelfLayoutNums = bookShelfLayoutNums
        self.frame_noneBookShelf = frame_noneBookShelf

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.RightButton:
            # log.info("右击")
            # log.info("当前frame", self)
            mask_status = int(self.property("updating"))
            repair_status = int(self.property("repairing"))
            log.info(f"当前的遮罩层状态: {mask_status}")
            book_shelf_menu = QMenu_BookShelf(bookShelfNums=self.bookShelfLayoutNums,
                                              frame_bookShelf_NoBook=self.frame_noneBookShelf,
                                              parent=self,
                                              mask_status=mask_status,
                                              repair_status=repair_status)
            book_shelf_menu.breakSignal_bookinfo_menu.connect(self.call_toMain)
            book_shelf_menu.breakSignal_bookinfo_update_chapter.connect(self.call_update_chapter)
            book_shelf_menu.breakSignal_bookinfo_update_bookshelflayout.connect(self.call_updateBookShelfLayout)
            book_shelf_menu.breakSignal_bookinfo_repair_chapter.connect(self.call_repair_chapter)
            book_shelf_menu.breakSignal_delBookInDownloadLayout.connect(self.call_delbookindownloadlayout)
            book_shelf_menu.breakSignal_bookinfo_lessBookNums.connect(self.call_lessNums)
            book_shelf_menu.exec_(QCursor.pos())
        else:
            self.update()

    def mousePressEvent(self, e) -> None:
        pass

    def setLabelObject(self, label: QLabel):
        self.label_process = label

    def call_toMain(self, nums: int):
        self.breakSignal_bookinfo_frame.emit(nums, self.label_process)

    def call_delbookindownloadlayout(self, serialNumber: int, bookNums: int, status: int):
        self.breakSignal_delBookInDownloadLayout.emit(int(serialNumber), bookNums, status)

    def call_updateBookShelfLayout(self, s):
        self.breakSignal_bookinfo_update_bookShelfLayout.emit(s)

    def call_update_chapter(self, nums: int):
        self.breakSignal_bookinfo_update_chapter.emit(nums, self)

    def call_repair_chapter(self, nums: int):
        self.breakSignal_bookinfo_repair_chapter.emit(nums, self)

    def call_lessNums(self):
        self.breakSignal_bookinfo_lessBookNums.emit('')

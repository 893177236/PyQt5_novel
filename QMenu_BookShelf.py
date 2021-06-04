# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFrame, QMenu, QAction, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt, QFileInfo,QThread
from PyQt5.QtGui import QIcon
import re
import User
from QMessageBox_showMsg import QMessageBox_showMsg
from log import Logger

log = Logger().getlog()

class QMenu_BookShelf(QMenu):
    breakSignal_bookinfo_menu = pyqtSignal(int)
    breakSignal_bookinfo_lessBookNums = pyqtSignal(str)
    breakSignal_bookinfo_update_chapter = pyqtSignal(int)
    breakSignal_bookinfo_update_bookshelflayout = pyqtSignal(str)
    breakSignal_bookinfo_repair_chapter = pyqtSignal(int)
    breakSignal_delBookInDownloadLayout = pyqtSignal(int,int,int)
    def __init__(self, bookShelfNums: int, frame_bookShelf_NoBook: QFrame, mask_status: int, repair_status:int,parent=None):
        super().__init__()
        self.bookShelfNums = bookShelfNums
        self.frame_bookShelf_NoBook = frame_bookShelf_NoBook
        self.Frame: QFrame = parent
        self.setStyleSheet("""
        /*设置菜单样式*/
QMenu {
    background-color: rgba(243, 243, 243,0.7);
    /*background-color: white;*/
    font-size: 18px;
    font: 18px "Microsoft YaHei";
    padding: 5px 0px 16px 0px;
    border: 1px solid rgb(196, 199, 200);
    border-radius:0px;
}

QMenu::item {  
    padding: 7px 20px 7px 13px;
    /*background-color: transparent;*/
}
QMenu::icon{
    /*上  右   下   左    内边距
    padding: 0px 0px 0px 13px;
    */
    padding-right:13px;
    padding-left:8px;

}
QMenu::item:selected {
    border-width: 1px;
    border-color: rgb(212, 212, 212);
    background: rgb(200, 200, 200);
    color: black;
}

QMenu#lineEditMenu{
    /*width: 182px;*/
    width: 1px;
    border: 1px solid rgb(196, 199, 200);
    border-radius: 0px;
    padding: 5px 0px 5px 0px;
}
QMenu#lineEditMenu[hasCancelAct='true']{
    /*width: 213px;*/
    width: 1px;
}

QMenu#lineEditMenu::icon{
    position: absolute;
    left: 16px;
}

QMenu#lineEditMenu::item {
    padding-left: 26px;
}



        """)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground | Qt.WA_StyledBackground)

        bookInfo = QAction(u"书籍信息", self, triggered=self.showBookShelfBookInfo)
        bookInfo.setIcon(QIcon(QFileInfo("./Resource/icon/bookinfo128.png").absoluteFilePath()))

        updateChapter_text = u"更新中..." if mask_status == 1 else u"更新书籍"
        self.updateChapter = QAction(text=updateChapter_text, parent=self, triggered=self.updateBookChapter)
        self.updateChapter.setIcon(QIcon(QFileInfo("./Resource/icon/update128.png").absoluteFilePath()))

        repairChapter = u"修复中..." if repair_status == 1 else u"修复章节"
        self.repairChapter = QAction(text=repairChapter,parent=self,triggered=self.repairBookChapter)
        self.repairChapter.setIcon(QIcon(QFileInfo("./Resource/icon/repair128.png").absoluteFilePath()))

        removeFromBookShelf = QAction(u"移出书架", self, triggered=self.delBookShelfBook)
        removeFromBookShelf.setIcon(QIcon(QFileInfo("./Resource/icon/delete128.png").absoluteFilePath()))

        self.addAction(bookInfo)
        self.addAction(self.updateChapter)
        self.addAction(self.repairChapter)
        self.addAction(removeFromBookShelf)
        if mask_status == 1 or repair_status == 1:
            self.updateChapter.setEnabled(False)
            self.repairChapter.setEnabled(False)

    def showBookShelfBookInfo(self):
        book: QPushButton = self.Frame.findChild(QPushButton)
        bookPosition = re.findall(r"_\d+", book.objectName())

        bookNums = int(bookPosition[0].replace("_", ""))
        log.info(f"bookNums:{bookNums}")
        log.info("当前frame book 的objectname :%s"%book.objectName())

        self.breakSignal_bookinfo_menu.emit(bookNums)

    def updateBookChapter(self):
        log.info("更新章节")
        book: QPushButton = self.Frame.findChild(QPushButton)
        bookPosition = re.findall(r"_\d+", book.objectName())

        bookNums = int(bookPosition[0].replace("_", ""))
        log.info(f"bookNums:{bookNums}")
        log.info("当前frame book 的btnimage name :%s"%book.objectName())
        self.breakSignal_bookinfo_update_chapter.emit(bookNums)
    def repairBookChapter(self):
        log.info("修复章节")
        book:QPushButton = self.Frame.findChild(QPushButton)
        bookPosition = re.findall(r"_\d+", book.objectName())

        bookNums = int(bookPosition[0].replace("_", ""))
        log.info(f"bookNums:{bookNums}")
        log.info("当前frame book 的btnimage name :%s" % book.objectName())
        self.breakSignal_bookinfo_repair_chapter.emit(bookNums)
    def delBookShelfBook(self):
        msg = QMessageBox_showMsg(text="确定移出书架？", icon="")
        serialNumber = self.Frame.property("serialNumber")
        log.info("当前serialNumber:%s"%str(serialNumber))
        msg.addCheckBox(labeltext="同时删除本地文件")
        msg_states = msg.makeSures()
        if msg_states[0]:
            book: QPushButton = self.Frame.findChild(QPushButton)
            bookPosition = re.findall(r"_\d+", book.objectName())
            bookNums = int(bookPosition[0].replace("_", ""))
            self.Frame.parent().deleteLater()
            frame_bookshelf_line = self.Frame.parent().parent()  # 行frame
            frame_bookshelf_line_bookNums = len(frame_bookshelf_line.findChildren(QFrame, "frame_book"))
            log.info(f"当前所在行还剩余：{frame_bookshelf_line_bookNums}")
            if frame_bookshelf_line_bookNums == 0:  # 为0就是这一行没有书了。需要把行frame删掉
                log.info("这一行没有书了。需要把行frame删掉")
                frame_bookshelf_line.deleteLater()
            else:
                log.info("这一行还有书，无需删除")
            self.updateBookShelfLayoutBtnImageObjectName_Position()
            self.breakSignal_bookinfo_lessBookNums.emit('')
            self.breakSignal_bookinfo_update_bookshelflayout.emit('更新书架的书籍顺序')
            self.breakSignal_delBookInDownloadLayout.emit(serialNumber,bookNums,msg_states[1])

        else:
            log.info("取消移出书架")


    def updateBookShelfLayoutBtnImageObjectName_Position(self) -> None:  # 更新书架中书籍的图片objectName的定位bookNums
        bookshelf = self.Frame.parent().parent().parent().findChildren(QPushButton)
        currentBtnBook = self.Frame.findChild(QPushButton)
        log.info(f'书架的btn {str(bookshelf)}')
        log.info(f"当前的btn:{str(currentBtnBook)}")
        bookshelf.reverse()

        for btnImage in bookshelf:
            if btnImage == currentBtnBook:
                log.info("到了该行btn，退出循环")
                break
            btnImageObjName = btnImage.objectName()
            btnImagePosition = btnImageObjName.split("_")[-1]
            log.info(f"修改前objname bookNums: {btnImageObjName} {btnImagePosition}")
            newBtnImageObjName = f"btn_bookshelf_image_{int(btnImagePosition) - 1}"
            btnImage.setObjectName(newBtnImageObjName)
            log.info(f"修改后objname bookNums:{btnImage.objectName()},{int(btnImagePosition) - 1}")


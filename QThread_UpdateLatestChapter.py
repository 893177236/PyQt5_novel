# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep as time_sleep
from datetime import datetime
from catalog import Catalog
from content import Content
from QThread_PlayDownloadFinishSound import QThread_PlayDownloadFinishSound
from QMessageBox_showMsg import QMessageBox_showMsg
import User
from log import Logger
log = Logger().getlog()

class QThread_UpdateLatestChapter(QThread):
    breakSignal_showUpdating = pyqtSignal(object)
    breakSignal_setUpdatingResult = pyqtSignal(str, object)
    breakSignal_delUpdating = pyqtSignal(object)

    def __init__(self, bookNums: int, frame_image: QFrame):
        super().__init__(parent=None)
        self.bookNums = bookNums
        self.frame_image = frame_image

    def run(self) -> None:
        if (int(self.frame_image.property("updating")) == 1) or \
            (self.frame_image.property("frame_image_mask") is not None) or \
            (int(self.frame_image.property("repairing")) == 1):
            log.info("已有遮罩层")
            return
        log.info("开始！更新中遮罩层")
        self.frame_image.setProperty("updating", "1")
        self.breakSignal_showUpdating.emit(self.frame_image)
        # self.breakSignal_showUpdating.emit(False, self.frame_image)

        # time_sleep(3)
        # log.info("结束，关闭遮罩层")
        # self.frame_image.setProperty("updating", "0")
        # self.breakSignal_delUpdating.emit(self.frame_image)
        # return
        user = User.UserSql()
        book_info = user.selectBookShelfBookInfo(bookNums=self.bookNums)
        book_latest_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # log.info(bookInfo)
        if book_info is None:
            log.info("没有检索到书籍信息")
            QMessageBox_showMsg(text="检索本地书籍失败",icon="",title="更新章节").makeSure()
        else:
            book_path = book_info[3]
            book_url = book_info[11]
            book_rule = book_info[12]
            book_serial_number = book_info[13]

            log.info(f"{book_url}, {book_rule}, {book_serial_number}")
            catalog = Catalog(homeurl=book_url, whichRule=book_rule)
            catalog_main = catalog.main()
            catalog_main_nums = len(catalog_main)
            catalog_already = self.getChapterTotalNums(serialNumber=book_serial_number)
            log.info(str(catalog_main))
            if catalog_main_nums == 0:
                log.info("检索失败，章节为0")
                self.breakSignal_setUpdatingResult.emit("./Resource/update_failed128.png", self.frame_image)
                time_sleep(3)
            elif catalog_main_nums > catalog_already:
                log.info(f"确认有新章节,本地章节数:{catalog_already},网络请求到的章节数:{catalog_main_nums}")
                new_chapter = catalog_main[catalog_already:]
                if len(new_chapter):
                    for i in range(len(new_chapter)):
                        chapter_url = new_chapter[i]["bookUrl"]
                        chapter_name = new_chapter[i]["chapterName"]
                        chapter_content = self.getChapterContent(
                            priority=i, chapterUrl=chapter_url,
                            chapterName=chapter_name, whichRule=book_rule)
                        self.updateSqlBookInfoNewChapterInfo(
                            chapterName=chapter_name, chapterContent=chapter_content[1],
                            chapterSerialNumber=book_serial_number)
                        self.updateLocalTextNewChapterInfo(
                            bookPath=book_path, chapterName=chapter_name,
                            chapterContent=chapter_content[0])
                    self.updateSqlBookShelfNewInfo(
                        bookLatestChapter=new_chapter[-1]["chapterName"],
                        bookLatestUpdateTime=book_latest_update_time,
                        bookSerialNumber=book_serial_number)
                    self.playFinishSound()
                else:
                    log.info("新章节数量为0")
                self.breakSignal_setUpdatingResult.emit("./Resource/update_success128.png", self.frame_image)
                time_sleep(3)
            else:
                log.info("无需更新")
        # self.breakSignal_changeUpdatingStatusProperty.emit("0",self.frame_image)
        # self.breakSignal_showUpdating.emit(False, self.frame_image)
        log.info("结束，关闭遮罩层")
        self.frame_image.setProperty("updating", "0")
        self.breakSignal_delUpdating.emit(self.frame_image)

    def playFinishSound(self):
        self.threadMusic = QThread_PlayDownloadFinishSound()
        self.threadMusic.start()

    @staticmethod
    def getChapterTotalNums(serialNumber: int) -> int:
        user = User.UserSql()
        total_nums = user.selectBookShelfChapterTotalNums(serialNumer=serialNumber)[0]
        return int(total_nums)

    @staticmethod
    def getChapterContent(priority: int, chapterUrl: str, chapterName: str, whichRule: int) -> list:  # 获取章节内容
        content = Content(priority=priority,
                          chapterName=chapterName,
                          chapterUrl=chapterUrl,
                          whichRule=whichRule)
        return content.chapterContent,content.chapterContentHTML

    @staticmethod
    def updateSqlBookInfoNewChapterInfo(chapterName: str, chapterContent: str, chapterSerialNumber: int):  # 数据库更新
        user = User.UserSql()
        user.insertNewChapterInfo(chapterName=chapterName,
                                  chapterContent=chapterContent,
                                  chapterSerialNumber=chapterSerialNumber)

    @staticmethod
    def updateSqlBookShelfNewInfo(bookLatestChapter: str, bookLatestUpdateTime: str, bookSerialNumber: int):
        user = User.UserSql()
        user.updateBookShelfNewInfo(bookLatestChapter=bookLatestChapter,
                                    bookLatestUpdateTime=bookLatestUpdateTime,
                                    bookSerialNumber=bookSerialNumber)

    @staticmethod
    def updateLocalTextNewChapterInfo(bookPath: str, chapterName: str, chapterContent: str):  # 本地文件追加
        with open(file=bookPath, mode="a+", encoding="utf-8") as f:
            f.write(chapterName)
            f.write("\n\n\n\n")
            f.write(chapterContent)
            f.write("\n\n\n\n\n\n\n\n")

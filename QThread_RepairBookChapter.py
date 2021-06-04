# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep as time_sleep
from datetime import datetime
from catalog import Catalog
from content import Content
from QThread_PlayDownloadFinishSound import QThread_PlayDownloadFinishSound
import User
import regular
from log import Logger

log = Logger().getlog()


class QThread_RepairBookChapter(QThread):
    breakSignal_showRepairing = pyqtSignal(object)
    breakSignal_delRepairing = pyqtSignal(object)
    breakSignal_sendRepairResult = pyqtSignal(str)
    breakSignal_setRepairingResult = pyqtSignal(object)

    def __init__(self, needRepairDict: dict, bookUrl: str, bookRule: int, frame_image: QFrame, delay_time: int,
                 serialNumber: int, autoRepair: int):
        super(QThread_RepairBookChapter, self).__init__()
        self.needRepairDict = needRepairDict
        self.needRepairNums = len(self.needRepairDict)
        self.bookUrl = bookUrl
        self.bookRule = bookRule
        self.frame_image = frame_image
        self.delay_time = delay_time
        self.serialNumber = serialNumber
        self.autoRepair = autoRepair

    def run(self) -> None:
        if (int(self.frame_image.property("updating")) == 1) or \
                (self.frame_image.property("frame_image_mask") is not None) or \
                (int(self.frame_image.property("repairing")) == 1):
            log.info("已有遮罩层")
            return

        log.info("开始！修复中遮罩层")
        self.frame_image.setProperty("repairing", "1")
        self.is_success = 0
        self.is_failed = 0
        self.breakSignal_showRepairing.emit(self.frame_image)

        catalog = Catalog(homeurl=self.bookUrl, whichRule=self.bookRule)
        self.catalog_main = catalog.main()
        catalog_main_nums = len(self.catalog_main)
        log.info(str(self.catalog_main))
        log.info(str(catalog_main_nums))
        if catalog_main_nums != 0:
            if self.autoRepair:
                self.auto()
            else:
                log.info("不自动修复")
                self.noauto()
        else:
            log.error("请求章节失败")

        self.breakSignal_delRepairing.emit(self.frame_image)
        self.playFinishSound()
        self.breakSignal_sendRepairResult.emit(
            f"需要修复{self.needRepairNums}章，成功{self.is_success}章，失败{self.is_failed}章")
        self.frame_image.setProperty("repairing", "0")

    def auto(self):
        localBook = self.selectBookInfoOriginalChapter(chapterSerialNumber=self.serialNumber)
        for bookinfo in localBook:
            chaptername: str = bookinfo[0]
            content: str = bookinfo[1]
            bookNum: int = bookinfo[2]
            requestChapterName = self.catalog_main[bookNum]['chapterName']
            requestChapterUrl = self.catalog_main[bookNum]['bookUrl']
            if (content.strip() == "") or (bookNum in self.needRepairDict):
                self.needRepairNums += 1
                log.info(f"serial:{self.serialNumber} 需要修复的章节内容:{chaptername}")
                if requestChapterName == chaptername:
                    self.is_success += 1
                    repaired_content = self.getChapterContent(priority=bookNum,
                                                              chapterUrl=requestChapterUrl,
                                                              chapterName=requestChapterName,
                                                              whichRule=self.bookRule)
                    self.updateSqlBookInfoOriginalChapterInfo(
                        chapterSerialNumber=self.serialNumber,
                        chapterContent=repaired_content,
                        chapterBookSerialNumber=bookNum
                    )
                    time_sleep(self.delay_time)
                else:
                    log.error(f"自动修复内容失败，章节名不匹配,{self.serialNumber} 原来：{chaptername},请求的{requestChapterName}")
                    self.is_failed += 1

    def noauto(self):
        for chapterNum, chapterName in self.needRepairDict.items():
            requestChapterName = self.catalog_main[chapterNum]['chapterName']
            requestChapterUrl = self.catalog_main[chapterNum]['bookUrl']
            if requestChapterName == chapterName:
                self.is_success += 1
                repaired_content = self.getChapterContent(priority=chapterNum,
                                                          chapterUrl=requestChapterUrl,
                                                          chapterName=requestChapterName,
                                                          whichRule=self.bookRule)
                self.updateSqlBookInfoOriginalChapterInfo(
                    chapterSerialNumber=self.serialNumber,
                    chapterContent=repaired_content,
                    chapterBookSerialNumber=chapterNum
                )
                time_sleep(self.delay_time)
            else:
                log.info("章节名称不同，不予更新")
                self.is_failed += 1

    @staticmethod
    def getChapterContent(priority: int, chapterUrl: str, chapterName: str, whichRule: int) -> str:  # 获取章节内容
        content = Content(priority=priority,
                          chapterName=chapterName,
                          chapterUrl=chapterUrl,
                          whichRule=whichRule)
        return content.chapterContentHTML

    @staticmethod
    def updateSqlBookInfoOriginalChapterInfo(chapterContent: str,
                                             chapterSerialNumber: int,
                                             chapterBookSerialNumber: int) -> None:  # 数据库更新
        user = User.UserSql()
        user.updateNewChapterInfo(chapterContent=chapterContent,
                                  chapterSerialNumber=chapterSerialNumber,
                                  chapterBookSerialNumber=chapterBookSerialNumber)

    @staticmethod
    def selectBookInfoOriginalChapter(chapterSerialNumber: int) -> list:
        user = User.UserSql()
        return user.selectBookInfoOriginalChapter(chapterSerialNumber=chapterSerialNumber)

    def playFinishSound(self) -> None:
        self.threadMusic = QThread_PlayDownloadFinishSound()
        self.threadMusic.start()

    def __getBookRule(self):
        return regular.Json().getData()[self.bookRule]

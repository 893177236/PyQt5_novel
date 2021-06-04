# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFrame
from PyQt5.Qt import QUrl, QFileInfo, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtNetwork import QNetworkProxyFactory
import json
from os import putenv
from User import UserSql
from log import Logger
import purify
log = Logger().getlog()
class ReadWindow(QMainWindow):
    breakSignal_updateBookShelfInfo = pyqtSignal(str)
    def __init__(self, serialNumber):
        super().__init__()
        if QFileInfo.exists("./read_debug.txt"):
            with open("./read_debug.txt", "r+") as f:
                putenv("QTWEBENGINE_REMOTE_DEBUGGING", f.read())
        self.setWindowTitle("阅读")
        self.setWindowIcon(QIcon(QFileInfo("./Resource/favicon.ico").absoluteFilePath()))
        self.browser = ReadWeb(serialNumber=serialNumber)
        BrowserWidth = self.browser.getLocalBookConf()["WindowWidth"]
        BrowserHeight = self.browser.getLocalBookConf()["WindowHeight"]
        if BrowserWidth and BrowserHeight:
            self.resize(int(BrowserWidth), int(BrowserHeight))
        vlayout_web = QVBoxLayout()
        QNetworkProxyFactory.setUseSystemConfiguration(False)
        frame = QFrame()
        vlayout_web.addWidget(self.browser)
        frame.setLayout(vlayout_web)
        vlayout_web.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(frame)
        self.setWindowIcon(QIcon(QFileInfo("./Resource/favicon.ico").absoluteFilePath()))
    def closeEvent(self, a0) -> None:
        self.breakSignal_updateBookShelfInfo.emit("")

    def resizeEvent(self, a0) -> None:
        self.browser.callSaveSetting("WindowWidth", f"{self.width()}")
        self.browser.callSaveSetting("WindowHeight", f"{self.height()}")


class ReadWeb(QWebEngineView):
    def __init__(self, serialNumber: int, parent=None):
        super(ReadWeb, self).__init__(parent)
        self.serialNumber = int(serialNumber)
        self.setReaderConf()
        self.initSetting()
        self.load(QUrl(QFileInfo("./read/novelread.html").absoluteFilePath()))

        self.channel = QWebChannel()

        # 把自身对象传递进去
        self.channel.registerObject('Bridge', self)
        # 设置交互接口
        self.page().setWebChannel(self.channel)
        # 开启不显示红色消息
        # qInstallMessageHandler((lambda *args: None))

    def setReaderConf(self):  # 从数据库中配置本地json当前页
        log.info("开始配置阅读数据")
        user = UserSql()
        currentPage = user.selectBookReaderCurrentPage(serialNumber=self.serialNumber)[0]
        scrollTop = user.selectBookReaderScrollTop(serialNumber=self.serialNumber)[0]
        # currentPage = user.updateReaderConf(currentPage=int(currentPage),serialNumber=int(serialNumber))
        self.callSaveSetting(key="currentPage", value=currentPage)
        self.callSaveSetting(key="currentPageScrollTop", value=scrollTop)
        log.info(f"当前阅读所在页：{currentPage},所在高度：{scrollTop}")
        log.info("配置本地json完毕")
    @pyqtSlot(str)
    def callFromJs_text(self, text):
        log.info("来自js调用：{}".format(text))

    def initSetting(self):  # 初始化设置
        setting = QWebEngineSettings.globalSettings()
        setting.setDefaultTextEncoding("utf-8")
        setting.setAttribute(
            QWebEngineSettings.JavascriptCanAccessClipboard, True)
        # 支持图标触摸,默认关闭
        setting.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
    def getBookInfo(self) -> list:
        user = UserSql()
        contentList = user.selectReadBookInfo(chapterSerialNumber=self.serialNumber)
        log.info("内容长度%d"%len(contentList))
        return contentList

    @pyqtSlot(str, str)
    def callSaveSetting(self, key: str, value: str):
        settingConf = self.getLocalBookConf()
        settingConf["%s" % key] = f"{value}"
        self.setLocalBookConf(settingConf)

        if key == "currentPage":
            self.updateSqliteProgress(int(value))
        if key == "currentPageScrollTop":
            self.updateSqliteCurrentPageScrollTop(serialNumber=self.serialNumber, scrollTop=int(value))

    def updateSqliteProgress(self, currentPage: int):  # 设置数据库中当前书籍的进度
        user = UserSql()
        MAXChapterNum = user.selectBookReaderMaxNum(serialNum=self.serialNumber)
        progress = round(currentPage / int(MAXChapterNum[0]), 2)
        user.updateBookReaderProgress(progress=progress, serialNum=self.serialNumber)
        user.updateReaderConf(serialNumber=self.serialNumber, currentPage=currentPage)

    def updateSqliteCurrentPageScrollTop(self, serialNumber: int, scrollTop: int):  # 设置数据库中当前书籍的高度
        user = UserSql()
        user.updateReaderConfScrollTop(scrollTop=scrollTop, serialNumber=serialNumber)

    def setLocalBookConf(self, newConf) -> None:  # 设置本地阅读器设置
        with open(file=QFileInfo("./read/conf/setting.json").absoluteFilePath(), mode="w+", encoding="utf8") as f:
            f.write(json.dumps(newConf))

    def getLocalBookConf(self) -> dict:  # 读取本地阅读器设置
        with open(file=QFileInfo("./read/conf/setting.json").absoluteFilePath(), mode="r+", encoding="utf8") as f:
            return json.load(f)

    @pyqtSlot(str, result=list)
    def bookInfo(self) -> list:
        bookList = []
        for bookinfo in self.getBookInfo():
            bookDict = {
                "chapterNum": int(bookinfo[0]) + 1,
                "chapterName": "%s" % bookinfo[1],
                "chapterContent": "%s" % bookinfo[2]
            }
            bookList.append(bookDict)
        return bookList

    @pyqtSlot(str,result=list)
    def purifyInfo(self)->list:
        purifyinfo = purify.Json().getData()
        log.info(f"加载净化规则{str(purifyinfo)}")
        return purifyinfo

    @pyqtSlot(int, result=int)
    def currentPage(self) -> int:
        settingConf = self.getLocalBookConf()
        return int(settingConf["currentPage"]) if settingConf["currentPage"] != "" else 1

    getPurifyInfo = pyqtProperty(list,fget=purifyInfo)
    getArrayBookInfo = pyqtProperty(list, fget=bookInfo)
    getCurrentPage = pyqtProperty(int, fget=currentPage)


# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from mock_useragent import UserAgent
from datetime import datetime
import re
import json
import requests


class QThread_Xpath(QThread):
    breakSignal_appendResultText = pyqtSignal(str)
    breakSignal_insertResultHTML = pyqtSignal(str)
    breakSignal_setHTML = pyqtSignal(str)

    def __init__(self, url: str, charset: str, method: int, headers: str, data: str):
        super().__init__()
        self.url_user = url.strip()
        self.charset_user = charset.strip()
        self.method_user = method
        self.headers_user = headers
        self.data_user = data

    def run(self) -> None:
        self.headers = {
            "User-Agent": UserAgent().random_chrome
        }
        self.data = {}
        if self.checkParams() is True:
            self.addInfo("检索完毕,开始请求url")
            if self.method_user == 0:  # 0是get 1是post
                self.addInfo("当前请求为GET")
                html = self.getHTML()
            else:
                self.addInfo("当前请求为POST")
                self.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
                html = self.postHTML()
            self.addInfo(html)
            self.breakSignal_setHTML.emit(html)
            # self.breakSignal_appendResultText.emit(html)
        else:
            self.addInfo("检索完毕，当前仍有数据不符合规格，不予请求")

    def appendResultText(self, text: str) -> None:
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.breakSignal_appendResultText.emit(f"{now_time}: {text}")

    def insertResultHTML(self, text: str) -> None:
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.breakSignal_insertResultHTML.emit(f"<font color='red'>{now_time}:</font> {text}<br />")

    def addInfo(self, text: str) -> None:
        self.appendResultText(text)
        self.insertResultHTML(text)

    def checkParams(self) -> bool:  # 检查各个数据是否能够运行
        return self.checkUrl() and self.checkCharset() and self.checkHeaders() and self.checkData()

    def checkUrl(self) -> bool:
        if self.url_user != "":
            url_match = re.findall(r"http(s|)://.+", self.url_user, re.S)
            if url_match:
                self.addInfo(f"url => {self.url_user}")
                return True
            else:
                self.addInfo("输入的不是url")
                return False
        else:
            self.addInfo("输入的url不能为空")
            return False

    def checkCharset(self) -> bool:
        if self.charset_user != "":
            self.addInfo(f"charset => {self.charset_user}")
            return True
        else:
            self.addInfo("charset => 无，默认为返回")
            return True

    def checkHeaders(self) -> bool:  # 检索headers头
        if self.headers_user != "":
            try:
                parse_headers = json.loads(self.headers_user)
                self.headers.update(parse_headers)
                self.addInfo(f"当前headers => {str(self.headers)}")
                return True
            except Exception:
                self.addInfo("输入的headers格式不正确，使用默认headers")
                self.addInfo(f"当前headers => {str(self.headers)}")
                return False
        else:
            self.addInfo("不需要添加其他的headers")
            self.addInfo(f"当前headers => {str(self.headers)}")
            return True

    def checkData(self) -> bool:
        if self.data_user != "":
            try:
                parse_data = json.loads(self.data_user)
                self.data.update(parse_data)
                self.addInfo(f"data => {str(self.data)}")
                return True
            except Exception:
                self.addInfo("输入的data字典格式不正确")
                return False
        else:
            self.addInfo("data为空，不需要添加")
            return True

    def getHTML(self) -> str:
        html = requests.get(url=self.url_user, headers=self.headers, verify=False)
        self.addInfo(f"status => {html.status_code}")
        if self.charset_user == "":
            return html.text
        else:
            try:
                decode_html = html.content.decode(self.charset_user)
            except UnicodeDecodeError:
                decode_html = ""
                self.addInfo(f"使用{self.charset_user}编码解码失败")
            return decode_html

    def postHTML(self) -> str:
        if len(self.data) == 0:
            html = requests.post(url=self.url_user, headers=self.headers,verify=False)
        else:
            html = requests.post(url=self.url_user, headers=self.headers, data=self.data,verify=False)
        self.addInfo(f"status => {html.status_code}")
        if self.charset_user == "":
            return html.text
        else:
            return html.content.decode(self.charset_user)

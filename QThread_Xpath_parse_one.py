# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from lxml import etree
from log import Logger
log = Logger().getlog()

class QThread_Xpath_parse_one(QThread):
    breakSignal_insertTestXpathHTML = pyqtSignal(str)

    def __init__(self, xpath: str, responseHTMl: str):
        super().__init__()
        self.xpath_user = xpath.strip()
        self.responseHTMl = responseHTMl

    def run(self) -> None:
        if self.responseHTMl != "":
            if self.xpath_user != "":
                log.info(f"xpath语法:{self.xpath_user}")
                self.insertTestXpathHTML(self.lxmlResp())
                # self.appendTestXpathText(self.lxmlResp())
            else:
                # self.appendTestXpathText("请先填入xpath语法")
                self.insertTestXpathHTML("请先填入xpath语法")
        else:
            self.insertTestXpathHTML("请先请求url再执行xpath")

    # def appendTestXpathText(self, text) -> None:
    #     self.breakSignal_appendTestXpathText.emit(f"{text}")
    def insertTestXpathHTML(self, text: str) -> None:
        self.breakSignal_insertTestXpathHTML.emit(text)

    def lxmlResp(self) -> str:
        html = etree.HTML(self.responseHTMl)
        try:
            xpath_get = ""
            xpath_list = html.xpath(self.xpath_user)
            self.insertTestXpathHTML(
                f"<font color='red'>匹配到</font> {len(xpath_list)} <font color='red'>个结果</font><br />")
            for i in range(len(xpath_list)):
                if isinstance(xpath_list[i], etree._Element) is True:
                    xpath_list_ = str(xpath_list[i]).replace('<', '&lt;').replace('>', '&gt;')
                else:
                    xpath_list_ = str(xpath_list[i])
                xpath_get += f"<font color='red'>结果{i + 1}:</font> " + xpath_list_
                if i != len(xpath_list) - 1:
                    xpath_get += "<br />"
        except etree.XPathEvalError:
            xpath_get = "<font color='red'>非法的xpath语法</font><br />"
        return str(xpath_get)

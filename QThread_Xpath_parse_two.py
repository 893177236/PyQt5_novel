# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
from lxml import etree
from log import Logger
log = Logger().getlog()

class QThread_Xpath_parse_two(QThread):
    breakSignal_insertTestXpathHTML = pyqtSignal(str)

    def __init__(self, element: str, xpath: str, responseHTMl: str):
        super().__init__()
        self.element_user = element.strip()
        self.xpath_user = xpath.strip()
        self.responseHTMl = responseHTMl

    def run(self) -> None:
        if self.responseHTMl != "":
            if self.element_user != "":
                log.info(f"xpath语法: {self.xpath_user}")
                self.lxmlResp()
            else:
                self.insertTestXpathHTML("请先填入根节点语法")
        else:
            self.insertTestXpathHTML("请先请求url再执行xpath")

    def insertTestXpathHTML(self, text: str) -> None:
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.breakSignal_insertTestXpathHTML.emit(f"<font color='red'>{now_time}:</font> {text}<br />")

    def insertTestXpathHTMLNoTime(self, text: str) -> None:
        self.breakSignal_insertTestXpathHTML.emit(text)

    def lxmlResp(self):
        html = etree.HTML(self.responseHTMl)
        try:
            parent_element = html.xpath(self.element_user)
            self.insertTestXpathHTML(f"匹配到根节点 {len(parent_element)} 个")
            self.insertTestXpathHTML(f"{str(parent_element).replace('<', '&lt;').replace('>', '&gt;')}")
            for i in range(len(parent_element)):
                child_element = parent_element[i]
                if isinstance(child_element, etree._Element) is True:
                    if self.xpath_user == "":
                        self.insertTestXpathHTML("当前没有设置子节点语法")
                        break
                    child = child_element.xpath(self.xpath_user)
                    self.insertTestXpathHTML(f"父节点{i + 1}匹配到的子节点结果: {len(child)} 个")
                    self.insertTestXpathHTMLNoTime(f"{str(child)}")
                else:
                    self.insertTestXpathHTML("非法的根节点语法")
                    break
        except etree.XPathEvalError:
            self.insertTestXpathHTML("解析失败")

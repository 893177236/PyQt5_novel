# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from mock_useragent import UserAgent
import requests
import json
import purify
from log import Logger
log = Logger().getlog()

class QThread_PurifyReadNetRule(QThread):
    breakSignal_updatePurifyRuleLayout = pyqtSignal(str)

    def __init__(self, netJsonLink: str):
        super().__init__()
        self.netJsonLink = netJsonLink

    def run(self):
        headers = {
            "User-Agent": UserAgent().random_chrome
        }
        log.info(f"用户输入网络json文件：{self.netJsonLink}")
        try:
            net_json = requests.get(url=self.netJsonLink, headers=headers, timeout=10, verify=False)
            net_json_json = json.loads(net_json.text)
            self.setLocalPurifyJsonRule(rule=net_json_json)
            self.breakSignal_updatePurifyRuleLayout.emit("")
        except requests.Timeout:
            log.info("获取json文件超时")

    @staticmethod
    def setLocalPurifyJsonRule(rule: str):
        local_purify_json = purify.Json()
        local_purify_json.setData(json.dumps(rule))
        log.info("读取网络json完毕")

# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from mock_useragent import UserAgent
import requests
import json
import regular
from log import Logger
log = Logger().getlog()

class QThread_ReadNetRule(QThread):
    breakSignal_updateRuleLayout = pyqtSignal(str)

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
            self.setLocalJsonRule(rule=net_json_json)
            self.breakSignal_updateRuleLayout.emit("")
        except requests.Timeout:
            log.info("获取json文件超时")

    @staticmethod
    def setLocalJsonRule(rule: str):
        local_json = regular.Json()
        local_json.setData(json.dumps(rule))
        log.info("读取网络json完毕")

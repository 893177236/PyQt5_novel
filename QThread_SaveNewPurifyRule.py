# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QThread
import json
import purify
from log import Logger
log = Logger().getlog()

class QThread_SaveNewPurifyRule(QThread):  # 保存新的用户已创建的自定义规则文件数据
    breakSignal_isSuccess = pyqtSignal(str)

    def __init__(self, selectIndex: int, lineEdit_every_text: dict):
        super().__init__()
        self.selectIndex = selectIndex
        self.lineEdit_every_text = lineEdit_every_text

    def run(self) -> None:
        if self.selectIndex is not None:
            log.info("多线程...保存用户定义的净化规则数据")
            local_json_rule: list = self.getLocalPurifyJsonRule()
            need_update_json_rule = local_json_rule[self.selectIndex]
            need_update_json_rule.update(self.lineEdit_every_text)
            dump_user_data = json.dumps(local_json_rule)
            self.setLocalPurifyJsonRule(rule=dump_user_data)
            self.breakSignal_isSuccess.emit(self.lineEdit_every_text["purifySourceName"])
        else:
            log.info("获取当前的规则所在row失败")

    @staticmethod
    def setLocalPurifyJsonRule(rule: str):
        local_purify_json = purify.Json()
        local_purify_json.setData(rule)

    @staticmethod
    def getLocalPurifyJsonRule() -> list:
        local_purify_json = purify.Json()
        purify_data = local_purify_json.getData()  # 初始化自定义规则
        return purify_data

# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
import json
import regular
import purify
from log import Logger
log = Logger().getlog()

class QThread_UpdateUserRuleEnable(QThread):  # 更新规则启用状态(默认2启用)
    breakSignal_isSuccess = pyqtSignal(bool)

    def __init__(self, enable: int, selectIndex: int):
        super().__init__()
        self.enable = enable
        self.selectIndex = selectIndex

    def run(self) -> None:
        log.info(f"当前更新的规则所在行 {str(self.selectIndex)}")
        local_json_rule: list = self.getLocalJsonRule()
        local_json_rule[self.selectIndex]["enable"] = self.enable
        dump_user_data = json.dumps(local_json_rule)
        self.setLocalJsonRule(rule=dump_user_data)
        if self.enable:
            self.breakSignal_isSuccess.emit(True)
        else:
            self.breakSignal_isSuccess.emit(False)

    @staticmethod
    def setLocalJsonRule(rule: str):
        local_json = regular.Json()
        local_json.setData(rule)

    @staticmethod
    def getLocalJsonRule() -> list:
        local_json = regular.Json()
        user_data = local_json.getData()  # 初始化自定义规则
        return user_data

class QThread_UpdatePurifyRuleEnable(QThread):
    breakSignal_isSuccess = pyqtSignal(bool)

    def __init__(self, enable: int, selectIndex: int):
        super().__init__()
        self.enable = enable
        self.selectIndex = selectIndex

    def run(self) -> None:
        log.info(f"当前更新的净化规则所在行 {str(self.selectIndex)}")
        purify_json_rule: list = self.getPurifyJsonRule()
        purify_json_rule[self.selectIndex]["enable"] = self.enable
        dump_purify_data = json.dumps(purify_json_rule)
        self.setPurifyJsonRule(rule=dump_purify_data)
        if self.enable:
            self.breakSignal_isSuccess.emit(True)
        else:
            self.breakSignal_isSuccess.emit(False)

    @staticmethod
    def setPurifyJsonRule(rule: str):
        purify_json = purify.Json()
        purify_json.setData(rule)

    @staticmethod
    def getPurifyJsonRule() -> list:
        purify_json = purify.Json()
        purify_data = purify_json.getData()  # 初始化自定义规则
        return purify_data

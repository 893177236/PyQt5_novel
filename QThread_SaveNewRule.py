# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QThread
import json
import regular
from log import Logger
log = Logger().getlog()

class QThread_SaveNewRule(QThread):  # 保存新的用户已创建的自定义规则文件数据
    breakSignal_isSuccess = pyqtSignal(str)

    def __init__(self, selectIndex: int, lineEdit_every_text: dict):
        super().__init__()
        self.selectIndex = selectIndex
        self.lineEdit_every_text = lineEdit_every_text

    def run(self) -> None:
        if self.selectIndex is not None:
            log.info("多线程...保存用户定义的该数据")
            local_json_rule: list = self.getLocalJsonRule()
            need_update_json_rule = local_json_rule[self.selectIndex]
            need_update_json_rule.update(self.lineEdit_every_text)
            dump_user_data = json.dumps(local_json_rule)
            self.setLocalJsonRule(rule=dump_user_data)
            self.breakSignal_isSuccess.emit(self.lineEdit_every_text["bookSourceName"])
        else:
            log.info("获取当前的规则所在row失败")

    @staticmethod
    def setLocalJsonRule(rule: str):
        local_json = regular.Json()
        local_json.setData(rule)

    @staticmethod
    def getLocalJsonRule() -> list:
        local_json = regular.Json()
        user_data = local_json.getData()  # 初始化自定义规则
        return user_data

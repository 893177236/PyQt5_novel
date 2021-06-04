# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread
import json
import purify
from log import Logger

log = Logger().getlog()


class QThread_AddNewPurify(QThread):
    def __init__(self, newPurifyName: str):
        super(QThread_AddNewPurify, self).__init__()
        self.newPurifyName = newPurifyName

    def run(self) -> None:
        purify_rule = '''{
                      "enable":0,
                      "purifySourceName": "%s",
                      "replaceRule":"",
                      "isRexp":0,
                      "replaceAfterText":""
                    }''' % self.newPurifyName
        purify_data = self.getPurifyJsonRule()
        purify_data.append(json.loads(purify_rule))
        dump_purify_data = json.dumps(purify_data)
        log.info(f"type:{type(dump_purify_data)}")
        self.setPurifyJsonRule(rule=dump_purify_data)

    @staticmethod
    def setPurifyJsonRule(rule: str) -> None:
        local_purify_json = purify.Json()
        local_purify_json.setData(rule)

    @staticmethod
    def getPurifyJsonRule() -> list:
        local_purify_json = purify.Json()
        purify_data = local_purify_json.getData()  # 初始化自定义规则
        return purify_data
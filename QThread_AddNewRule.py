# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread
import json
import regular
from log import Logger
log = Logger().getlog()

class QThread_AddNewRule(QThread):  # 添加新的用户自定义规则文件
    def __init__(self, newRuleName: str):
        super().__init__()
        self.newRuleName = newRuleName

    def run(self) -> None:
        rule = '''{
              "enable":0,
              "bookSourceName": "%s",
              "bookSourceUrl": "",
              "searchUrl": "",
              "charset": "",
              "method": 0,
              "data": "",
              "searchBook": {
                "element": "",
                "toUrl": "",
                "image": "",
                "bookname": "",
                "author": "",
                "endstate": "",
                "latestChapter": "",
                "updateTime": "",
                "content": "",
                "noneSearch": "",
                "onlySearch": {
                  "isOnlySearch": 0,
                  "element": "",
                  "toUrl": "",
                  "image": "",
                  "bookname":"",
                  "author": "",
                  "endstate":"",
                  "latestChapter":"",
                  "updateTime": "",
                  "content": ""
                }
              },
              "catalog": {
                "model": 2,
                "nextPage":"",
                "toUrl": "",
                "element": "",
                "bookUrl": "",
                "chapterName": "",

                "ajax": {
                    "url": "",
                    "method": "",
                    "data": ""
                }
              },
              "content": {
                "text": ""
              }
            }''' % self.newRuleName
        user_data = self.getLocalJsonRule()
        user_data.append(json.loads(rule))
        dump_user_data = json.dumps(user_data)
        log.info(f"type:{type(dump_user_data)}")
        self.setLocalJsonRule(rule=dump_user_data)

    @staticmethod
    def setLocalJsonRule(rule: str) -> None:
        local_json = regular.Json()
        local_json.setData(rule)

    @staticmethod
    def getLocalJsonRule() -> list:
        local_json = regular.Json()
        user_data = local_json.getData()  # 初始化自定义规则
        return user_data

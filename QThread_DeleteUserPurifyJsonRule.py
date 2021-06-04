# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread
import json
import purify


class QThread_DeleteUserPurifyJsonRule(QThread):  # 删除需要删除的用户自定义规则文件
    def __init__(self, needRemoveIndex):
        super().__init__()
        self.needRemoveIndex = needRemoveIndex

    def run(self) -> None:
        user = purify.Json()
        local_purify_rule = user.getData()
        for index in self.needRemoveIndex:
            local_purify_rule.pop(index)
        user.setData(json.dumps(local_purify_rule))

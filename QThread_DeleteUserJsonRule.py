# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread
import json
import regular


class QThread_DeleteUserJsonRule(QThread):  # 删除需要删除的用户自定义规则文件
    def __init__(self, needRemoveIndex):
        super().__init__()
        self.needRemoveIndex = needRemoveIndex

    def run(self) -> None:
        user = regular.Json()
        local_rule = user.getData()
        for index in self.needRemoveIndex:
            local_rule.pop(index)
        user.setData(json.dumps(local_rule))

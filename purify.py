# -*- coding: utf-8 -*-
import regular
import os
from log import Logger

log = Logger().getlog()


class Json(regular.Json):

    def __init__(self):
        super(Json, self).__init__()
        self.checkRule()

    def checkRule(self) -> None:
        self.setPath(os.getcwd() + "/bookPurify.json")
        if self.checkFile() is True:
            pass
        else:
            log.info("本地净化json文件不存在，创建")
            self.createRuleJson()

Json()

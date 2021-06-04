# -*- coding: utf-8 -*-
import json
import os
from log import Logger
log = Logger().getlog()

class Json:
    def __init__(self):
        self.checkRule()

    def checkFile(self) -> bool:  # 检索本地json文件存在状态
        return True if os.path.isfile(self.getPath()) else False

    def checkRule(self) -> None:  # 例行检查
        self.setPath(os.getcwd() + "/bookSource.json")
        if self.checkFile() is True:
            pass
        else:
            log.info("本地json文件不存在，创建")
            self.createRuleJson()

    def setData(self, newRegular) -> None:  # 设置本地json数据
        with open(self.getPath(), 'w+', encoding="utf8") as f:
            f.write(str(newRegular))

    def getData(self) -> list:  # 获取本地json数据
        try:
            with open(self.getPath(), 'r+', encoding="utf8") as f:
                regular = json.load(f)

            return regular
        except json.decoder.JSONDecodeError:
            log.error(f"解析{self.getPath()}失败")
            return []

    def setPath(self, path: str) -> None:  # 设置json路径
        self._path = path

    def getPath(self) -> str:  # 获取json路径
        return self._path

    def createRuleJson(self):
        rule ='[]'
        with open(self.getPath(), "w+", encoding="utf-8") as f:
            f.write(str(json.loads(rule)))

# Json().getData()

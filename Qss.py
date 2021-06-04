# -*- coding: utf-8 -*-
class Qss:  # 加载qss文件
    @staticmethod
    def readQss(style) -> str:
        with open(style, 'r', encoding="utf-8") as f:
            return f.read()

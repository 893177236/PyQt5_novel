# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from log import Logger

log = Logger().getlog()


class QThread_ReadPurifyRule(QThread):
    breakSignal_setPurifyLayoutData = pyqtSignal(str, str, int, str)

    def __init__(self, now_purify_rule: dict):
        super().__init__()
        self.now_purify_rule = now_purify_rule

    def run(self) -> None:
        try:
            log.info("当前读取到的净化规则%s" % str(self.now_purify_rule))
            purify_enable = self.now_purify_rule["enable"]
            line_edit_source_name = self.now_purify_rule["purifySourceName"]
            purify_replaceRule = self.now_purify_rule["replaceRule"]
            purify_isRexp = self.now_purify_rule["isRexp"]
            purify_replaceAfterText = self.now_purify_rule["replaceAfterText"]

            self.breakSignal_setPurifyLayoutData.emit(line_edit_source_name,
                                                      purify_replaceRule,
                                                      purify_isRexp,
                                                      purify_replaceAfterText)
        except Exception as err:
            log.error(err)

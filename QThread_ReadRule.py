# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QTextEdit, QRadioButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from log import Logger

log = Logger().getlog()


class QThread_ReadRule(QThread):
    breakSignal_setUserRuleData = pyqtSignal(list)
    breakSignal_setUserRuleData_model_1 = pyqtSignal(list)
    breakSignal_setUserRuleData_model_2 = pyqtSignal(list)
    breakSignal_setUserRuleData_model_3 = pyqtSignal(list)
    breakSignal_setUserRuleData_model_4 = pyqtSignal(list)
    breakSignal_setUserRuleData_model_5 = pyqtSignal(list)
    breakSignal_setUserRuleData_only_search = pyqtSignal(list)
    breakSignal_setUserRuleData_no_only_search = pyqtSignal(str)
    breakSignal_clearControlsText = pyqtSignal(str)
    breakSignal_setCursorPositon = pyqtSignal(str)

    def __init__(self, now_rule: dict):
        super().__init__()
        self.now_rule = now_rule

    def run(self) -> None:
        try:
            self.breakSignal_clearControlsText.emit("")
            data = [
                self.now_rule["bookSourceName"],
                self.now_rule["bookSourceUrl"],
                self.now_rule["searchUrl"],
                self.now_rule["charset"],
                self.now_rule["method"],
                self.now_rule["data"],
                self.now_rule["searchBook"]["element"],
                self.now_rule["searchBook"]["toUrl"],
                self.now_rule["searchBook"]["image"],
                self.now_rule["searchBook"]["bookname"],
                self.now_rule["searchBook"]["author"],
                self.now_rule["searchBook"]["endstate"],
                self.now_rule["searchBook"]["latestChapter"],
                self.now_rule["searchBook"]["updateTime"],
                self.now_rule["searchBook"]["content"],
                self.now_rule["searchBook"]["noneSearch"],
                self.now_rule["content"]["text"]
            ]
            self.breakSignal_setUserRuleData.emit(data)
            model = self.now_rule["catalog"]["model"]
            if model == 1:
                data_model = [
                    self.now_rule["catalog"]["element"],
                    self.now_rule["catalog"]["bookUrl"],
                    self.now_rule["catalog"]["chapterName"]
                ]
                self.breakSignal_setUserRuleData_model_1.emit(data_model)
            elif model == 2:
                data_model = [
                    self.now_rule["catalog"]["toUrl"],
                    self.now_rule["catalog"]["element"],
                    self.now_rule["catalog"]["bookUrl"],
                    self.now_rule["catalog"]["chapterName"]
                ]
                self.breakSignal_setUserRuleData_model_2.emit(data_model)
            elif model == 3:
                data_model = []
                self.breakSignal_setUserRuleData_model_3.emit(data_model)
            elif model == 4:
                if self.now_rule["catalog"]["ajax"]["method"] == 1:
                    method = 1
                else:
                    method = 2
                data_model = [
                    self.now_rule["catalog"]["toUrl"],
                    self.now_rule["catalog"]["element"],
                    self.now_rule["catalog"]["bookUrl"],
                    self.now_rule["catalog"]["chapterName"],
                    self.now_rule["catalog"]["ajax"]["url"],
                    method,
                    self.now_rule["catalog"]["ajax"]["data"]
                ]
                self.breakSignal_setUserRuleData_model_4.emit(data_model)
            else:
                data_model = [
                    self.now_rule["catalog"]["nextPage"],
                    self.now_rule["catalog"]["element"],
                    self.now_rule["catalog"]["bookUrl"],
                    self.now_rule["catalog"]["chapterName"]
                ]
                self.breakSignal_setUserRuleData_model_5.emit(data_model)
            if int(self.now_rule["searchBook"]["onlySearch"]["isOnlySearch"]):
                data_only_search = [
                    self.now_rule["searchBook"]["onlySearch"]["element"],
                    self.now_rule["searchBook"]["onlySearch"]["toUrl"],
                    self.now_rule["searchBook"]["onlySearch"]["image"],
                    self.now_rule["searchBook"]["onlySearch"]["bookname"],
                    self.now_rule["searchBook"]["onlySearch"]["author"],
                    self.now_rule["searchBook"]["onlySearch"]["endstate"],
                    self.now_rule["searchBook"]["onlySearch"]["latestChapter"],
                    self.now_rule["searchBook"]["onlySearch"]["updateTime"],
                    self.now_rule["searchBook"]["onlySearch"]["content"]
                ]
                self.breakSignal_setUserRuleData_only_search.emit(data_only_search)
            else:
                self.breakSignal_setUserRuleData_no_only_search.emit("")

            self.breakSignal_setCursorPositon.emit("")

        except Exception as err:
            log.error(err)

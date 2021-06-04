# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo
from ui.readNetJson import Ui_Dialog
from QWidget_Mask import QWidget_Mask
from log import Logger
log = Logger().getlog()

class QDialog_ReadNetJson(QDialog, Ui_Dialog):  # 用户输入网络json的弹窗
    def __init__(self, Windows):
        super(QDialog_ReadNetJson, self).__init__()
        self.setWindowIcon(QIcon(QFileInfo("./Resource/favicon.ico").absoluteFilePath()))
        self.setupUi(self)
        self.Windows = Windows
        self.Mask = QWidget_Mask(self.Windows)
        self.Mask.show()

    def closeEvent(self, a0) -> None:
        log.info("关闭")
        self.Mask.close()

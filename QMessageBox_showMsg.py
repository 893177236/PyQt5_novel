# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox, QLabel, QCheckBox, QGridLayout
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QIcon, QPixmap, QFont
from Qss import Qss
from QWidget_Mask import QWidget_Mask
import os
from log import Logger
log = Logger().getlog()

class QMessageBox_showMsg(QMessageBox):
    def __init__(self, title: str = "提示", icon: str = "./Resource/errror.jpeg", text: str = "", Windows=None):
        super(QMessageBox_showMsg, self).__init__()
        self.title = title
        self.icon = QFileInfo(icon).absoluteFilePath()
        self.text = text
        self.Windows = Windows
        self.initControls()

    def initControls(self) -> None:
        self.setWindowIcon(QIcon(QFileInfo("./Resource/favicon.ico").absoluteFilePath()))
        self.setWindowTitle(self.title)
        self.setText(self.text)
        self.setIconPixmap(QPixmap(self.icon).scaled(40, 40))
        self.setStyleSheet(Qss.readQss(QFileInfo("./Resource/messagebox.qss").absoluteFilePath()))
        textlabel = self.findChild(QLabel, "qt_msgbox_label")
        if textlabel:
            textlabel.setWordWrap(True)
            textlabel.adjustSize()
            textlabel.setAlignment(Qt.AlignVCenter)
        self.Mask = QWidget_Mask(self.Windows)

    def makeSure(self) -> None:
        self.addButton("确定", QMessageBox.AcceptRole)
        self.Mask.show()
        self.exec()
        try:
            self.Mask.close()
            log.info("关闭遮罩")
        except Exception as e:
            log.info("关闭遮罩失败%s"%e)

    def makeSures(self) -> list or int:
        self.addButton("确定", QMessageBox.AcceptRole)
        self.addButton("取消", QMessageBox.RejectRole)
        self.Mask.show()
        self.exec()
        if self.clickedButton().text() == "确定":
            status = 1
        else:
            status = 0
        try:
            self.Mask.close()
            log.info("关闭遮罩")
        except Exception as e:
            log.info("关闭遮罩失败%s"%e)
        checkbox: QCheckBox = self.findChild(QCheckBox)
        if checkbox:
            return status, checkbox.isChecked()
        else:
            return status

    def addCheckBox(self, labeltext: str = None):
        checkbox = QCheckBox()
        label = QLabel()
        label.setFont(QFont("Microsoft YaHei", 9))
        label.setText(labeltext)
        gridlayout: QGridLayout = self.layout()
        if os.path.isfile(self.icon):
            gridlayout.addWidget(checkbox, 1, 1)
            gridlayout.addWidget(label, 1, 2)

        else:
            gridlayout.addWidget(checkbox, 1, 0)
            gridlayout.addWidget(label, 1, 1)

    def hideIcon(self) -> None:
        self.setIcon(QMessageBox.NoIcon)

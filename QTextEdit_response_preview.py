# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextEdit, QFrame, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent
from log import Logger
log = Logger().getlog()

class QTextEdit_response_preview(QTextEdit):
    def __init__(self, frame_findtext: QFrame, lineEdit_getUserFindText: QLineEdit):
        super().__init__()
        self.frame_findtext = frame_findtext
        self.lineEdit_getUserFindText = lineEdit_getUserFindText
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFont(QFont("Microsoft YaHei", 9))

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F:
            log.info("组合按键")
            log.info("显示搜索框")
            if self.frame_findtext.isHidden():
                self.frame_findtext.show()
                self.lineEdit_getUserFindText.setFocus()
            else:
                self.frame_findtext.hide()

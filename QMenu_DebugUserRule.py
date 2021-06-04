# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFrame, QMenu, QAction
from PyQt5.QtCore import pyqtSignal, Qt, QFileInfo
from PyQt5.QtGui import QIcon
from log import Logger
log = Logger().getlog()

class QMenu_DebugUserRule(QMenu):
    breakSignal_toDebugInterface = pyqtSignal(int)

    def __init__(self, whichRule: int, parent=None):
        super().__init__()
        self.whichRule = whichRule
        self.Frame: QFrame = parent
        self.setStyleSheet("""
/*设置菜单样式*/
QMenu {
    background-color: rgba(243, 243, 243,0.7);
    /*background-color: white;*/
    font-size: 18px;
    font: 18px "Microsoft YaHei";
    padding: 5px 0px 16px 0px;
    border: 1px solid rgb(196, 199, 200);
    border-radius:0px;
}

QMenu::item {  
    padding: 7px 20px 7px 13px;
    /*background-color: transparent;*/
}
QMenu::icon{
    /*上  右   下   左    内边距
    padding: 0px 0px 0px 13px;
    */
    padding-right:13px;
    padding-left:8px;

}
QMenu::item:selected {
    border-width: 1px;
    border-color: rgb(212, 212, 212);
    background: rgb(200, 200, 200);
    color: black;
}

QMenu#lineEditMenu{
    /*width: 182px;*/
    width: 1px;
    border: 1px solid rgb(196, 199, 200);
    border-radius: 0px;
    padding: 5px 0px 5px 0px;
}
QMenu#lineEditMenu[hasCancelAct='true']{
    /*width: 213px;*/
    width: 1px;
}

QMenu#lineEditMenu::icon{
    position: absolute;
    left: 16px;
}

QMenu#lineEditMenu::item {
    padding-left: 26px;
}
        """)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground | Qt.WA_StyledBackground)
        # debug_rule = QAction(text=u"调试", parent=self, triggered=self.debug)
        debug_rule = QAction(text=u"调试", parent=self)
        debug_rule.triggered.connect(self.debug)
        debug_rule.setIcon(QIcon(QFileInfo("./Resource/icon/debug128.png").absoluteFilePath()))
        self.addAction(debug_rule)

    def debug(self):
        log.info("开始调试")
        self.breakSignal_toDebugInterface.emit(self.whichRule)

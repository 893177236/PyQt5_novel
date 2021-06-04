# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
import User


class QThread_SelectLocalSQLDatabase(QThread):
    breakSignal_selectInfo = pyqtSignal(list)

    def __init__(self):
        super(QThread_SelectLocalSQLDatabase, self).__init__()

    def run(self) -> None:
        info = self.__select()
        if len(info) != 0:
            self.breakSignal_selectInfo.emit(info)

    @staticmethod
    def __select():
        user = User.UserSql()
        return user.selectIsInBookInfoDatabase()

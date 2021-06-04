# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread
import User


class QThread_DeleteUserLocalSQL(QThread):
    def __init__(self, select_serial_number: list):
        super().__init__()
        self.select_serial_number = select_serial_number

    def run(self) -> None:
        user = User.UserSql()
        for serialnumber in self.select_serial_number:
            user.deleteIsInBookInfoDatabase(serialNumber=int(serialnumber))

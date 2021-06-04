# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
import User
from log import Logger

log = Logger().getlog()

class QThread_UserData(QThread):
    breakSignal_str = pyqtSignal(str)
    breakSignal_UserData = pyqtSignal(str, int, int, str, int, int)

    def __init__(self, *args):
        super().__init__()
        self.args = args

    def run(self) -> None:
        user = User.UserSql()
        user.checkDefaultTable()  # 检索是否存在数据
        if len(self.args) == 6:
            user.updateUserInfo(savefilepath=self.args[0], progressnum=int(self.args[1]),
                                paralleltasks=int(self.args[2]), downloadfinishmusicpath=self.args[3],
                                downloadtaskdelaytime=self.args[4], searchProcessNum=self.args[5]
                                )
            self.breakSignal_str.emit('保存完毕')
        else:
            user.updateUserInfo()
            select = user.selectUserInfo()
            # self.breakSignal_str_str_str.emit(str(select[0]), str(select[1]), str(select[2]))
            self.breakSignal_UserData.emit(str(select["saveFilePath"]), int(select["progressNum"]),
                                           int(select["parallelTasks"]), str(select["downloadFinishMusicPath"]),
                                           int(select["downloadTaskDelayTime"]), int(select["searchProcessNum"]))


class threadUpdateUserSQLLeftWidget(QThread):  # 0为展开，1为缩小
    def __init__(self, status: int):
        super().__init__()
        self.status = status
    def run(self) -> None:
        log.info(f"设置布局left_widegt状态:{self.status} 0是完全体,1是缩小")
        user = User.UserSql()
        user.updateUserInfoLeftWidget(status=self.status)

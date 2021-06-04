# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
import winsound
import os
from QMessageBox_showMsg import QMessageBox_showMsg
from contextlib import closing as contextlib_closing
from wave import open as wave_open
from time import sleep as time_sleep
import User
from log import Logger

log = Logger().getlog()

class QThread_PlayDownloadFinishSound(QThread):
    breakSignal_stopPlay = pyqtSignal(str)

    def __init__(self, obj_lineEdit: QLineEdit = None):
        super(QThread_PlayDownloadFinishSound, self).__init__()
        self.obj_lineEdit = obj_lineEdit

    def run(self) -> None:
        path = self.obj_lineEdit.text() if self.obj_lineEdit else self.getFinishDownloadMusicPath()
        if os.path.isfile(path):
            log.info(f"播放wave:{path}")
            self.platWave(path)
        else:
            QMessageBox_showMsg(text=path + "音频不存在！", Windows=self).makeSure()
        self.breakSignal_stopPlay.emit('')

    def getFinishDownloadMusicPath(self) -> str:
        userSql = User.UserSql()
        result = userSql.selectFinishDownloadMusicPath()
        log.info(f"调用的检索数据库中的完成提示音: {str(result)} {type(result)}")
        return result

    def platWave(self, path):  # 播放wave音频
        with contextlib_closing(wave_open(path, 'rb')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            wav_length = frames / float(rate)
            log.info(f"音频长度：{str(round(wav_length, 1))}秒")
        # file = QUrl.fromLocalFile(path)  # 音频文件路径
        # content = QMediaContent(file)
        # self.player = QMediaPlayer()
        # self.player.setMedia(content)
        # self.player.setVolume(100)
        # self.player.play()
        winsound.PlaySound(path,winsound.SND_FILENAME|winsound.SND_ASYNC)
        time_sleep(round(wav_length, 1))

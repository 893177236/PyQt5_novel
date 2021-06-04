# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QMouseEvent, QMovie, QPixmap
from QThread_PlayDownloadFinishSound import QThread_PlayDownloadFinishSound


class QLabel_playSound(QLabel):
    def __init__(self, lineEdit_finishMusic: QLineEdit):
        super(QLabel_playSound, self).__init__()
        self.lineEdit_finishMusic = lineEdit_finishMusic
        self.setMinimumSize(20, 20)
        self.setMaximumSize(20, 20)
        self.setAlignment(Qt.AlignCenter)
        self.setClickImage()

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.setPlayMovie()
        self.threadMusic = QThread_PlayDownloadFinishSound(self.lineEdit_finishMusic)
        self.threadMusic.breakSignal_stopPlay.connect(self.setClickImage)
        self.threadMusic.start()

    def setPlayMovie(self) -> None:  # 播放音频事件

        audio_is_running = QMovie(":/icon/icon/refresh2.gif")  # 音频播放运行中提示
        audio_is_running.start()
        self.setMovie(audio_is_running)

    def setClickImage(self) -> None:
        play_audio = QPixmap(QFileInfo('./Resource/icon/playSound48.png').absoluteFilePath())
        self.setPixmap(play_audio)
        self.setScaledContents(True)

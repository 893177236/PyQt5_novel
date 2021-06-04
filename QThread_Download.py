# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QProgressBar, QLabel, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep as time_sleep
from datetime import datetime
from catalog import Catalog
from content import Content
from QThread_PlayDownloadFinishSound import QThread_PlayDownloadFinishSound
from queue import PriorityQueue
from concurrent.futures import ThreadPoolExecutor, as_completed
from novel_glob import get_value as global_get_value, set_value as global_set_value
import User
import os
import regular
from log import Logger

log = Logger().getlog()


class QThread_Download(QThread):
    breakSignal_obj_obj_obj = pyqtSignal(object, object, object)

    def __init__(self,
                 probar: QProgressBar, bookname: str,
                 lb_probar: QLabel, labelProgressState: QLabel,
                 btnAddBookToBookShelf: QPushButton, btnFile: QPushButton,
                 btnDel: QPushButton, lb_end: QLabel,
                 imagePath: str, homeurl: str,
                 taskSerialNumber: int, whichRule: int):  # 本地图片地址，主页地址，第N个规则

        super().__init__()

        self.probar = probar  # 进度条对象
        self.bookname = bookname  # 书名
        self.lb_probar = lb_probar  # 进度百分比对象
        self.labelProgressState = labelProgressState  # 进度文字对象
        self.btnAddBookToBookShelf = btnAddBookToBookShelf  # 阅读对象
        self.btnFile = btnFile  # 文件对象
        self.btnDel = btnDel  # 删除对象
        self.lb_end = lb_end  # 结束时间对象
        self.imagePath = imagePath  # 图片地址
        self.homeurl = homeurl  # 主目录url
        self.taskSerialNumber = taskSerialNumber  # 任务序列号
        self.rule = self.getRule()
        self.whichRule = int(whichRule)  # 第N个规则
        self.setDownloadTaskDelayTime()

    def run(self) -> None:
        # global parallelDownloadNums, nowDownloadNums
        # nowDownloadNums += 1
        number_of_download_tasks_now = global_get_value(key="number_of_download_tasks_now")
        number_of_download_tasks_now += 1
        number_of_parallel_download_tasks = global_get_value(key="number_of_parallel_download_tasks")
        global_set_value(key="number_of_download_tasks_now", value=number_of_download_tasks_now)
        self.labelProgressState.setText("正在等待其他队列...")
        log.info(f"当前任务数量：{number_of_download_tasks_now}")
        log.info(f"并行任务数量限制：{number_of_parallel_download_tasks}")
        log.info(f"当前任务延迟加载时间：{self.downloadTaskDelayTime}")
        while True:
            if number_of_download_tasks_now <= number_of_parallel_download_tasks:
                self.labelProgressState.setText("正在下载...")
                catalog_ = Catalog(homeurl=self.homeurl, whichRule=self.whichRule)
                catalog_get_main = catalog_.main()
                if catalog_get_main:
                    self.labelProgressState.setText("获取目录成功...")
                    thread_queue = PriorityQueue()  # 线程队列
                    # 获取目录列表的索引 组成列表 如[0,1,2,3,4,5,6...]
                    catalog_index = [index for index in range(0, len(catalog_get_main))]
                    catalog_progress = 0
                    save_file_location_path = self.getSaveFileLocation() + "/" + self.bookname + ".txt"
                    with ThreadPoolExecutor(max_workers=self.getProcessNums()) as t:
                        task_out_queue = []
                        for index in range(0, len(catalog_get_main)):
                            chapter_url = catalog_get_main[index]["bookUrl"]
                            chapter_name = catalog_get_main[index]["chapterName"]
                            log.info(f"章节名：{chapter_name},地址：{chapter_url}")
                            sub_args = (index, thread_queue, chapter_name, chapter_url)
                            task = t.submit(self.PutQueue, sub_args)
                            task_out_queue.append(task)
                        for queue in as_completed(task_out_queue):
                            data = queue.result()
                            if data in catalog_index:
                                catalog_index.remove(data)
                                catalog_progress += 1
                            progress = int(catalog_progress / len(catalog_get_main) * 100)
                            self.setProgressValue(progress)  # 设置progress控件进度
                            self.setLabelProbarProgress(progress)  # 设置progress控件后面的label控件信息进度
                            log.info(f"进度{progress}")
                            self.setLabelProbarState(f"正在下载...{catalog_progress}/{len(catalog_get_main)}")
                        log.info("获取完毕")
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.lb_end.setText(f"完成时间：{now}")
                        self.setLabelProbarState("正在处理文件...")

                        thread_queue_num = 0
                        thread_queue_qsize = int(thread_queue.qsize())
                        while not thread_queue.empty():
                            get_queue = thread_queue.get()
                            thread_queue_num += 1
                            file_process_progress = int(thread_queue_num / thread_queue_qsize * 100)
                            self.setLabelProbarState(f"正在处理文件...{file_process_progress}%")
                            log.info(f"取出标题：{get_queue.chapterName}")
                            user_sql = User.UserSql()

                            with open(save_file_location_path, "a+", encoding="utf-8") as f:
                                user_sql.insertChapterInfo(chapterName=get_queue.chapterName,
                                                           chapterContent=get_queue.chapterContentHTML,
                                                           chapterSerialNum=self.taskSerialNumber,  # 章节序号
                                                           chapterBookSerialNum=get_queue.priority  # 书籍标识序号  以时间决定
                                                           )
                                f.write(get_queue.chapterName)
                                f.write("\n\n\n\n")
                                f.write(get_queue.chapterContent)
                                f.write("\n\n\n\n\n\n\n\n")

                            # log.info(f"内容：{getQueue[1]}")
                    # self.btnAddBookToBookShelf.clicked.connect(lambda: self.addBookToBookShelf(saveFileLocationPath))
                    self.setLabelProbarState("已完成！")
                    self.updateSqlDownloadInfo(taskfinishtime=now, taskprogress=progress,
                                               taskstatusinfo="已完成!", taskbtnstatus=1,
                                               taskserialNumber=self.taskSerialNumber, taskprogresslabel=progress)
                    self.setBtnEnabled()
                    self.threadMusic = QThread_PlayDownloadFinishSound()
                    self.threadMusic.breakSignal_stopPlay.connect(self.call_playSound)
                    self.threadMusic.start()
                else:
                    self.setLabelProbarState("获取目录失败")
                    log.error("获取目录失败")
                number_of_download_tasks_now -= 1
                global_set_value(key="number_of_download_tasks_now", value=number_of_download_tasks_now)
                break
            else:
                log.info("等待中...")
                time_sleep(3)

    @staticmethod
    def call_playSound() -> None:  # 播放音频
        log.info("播放音频")

    def PutQueue(self, args: list) -> None:  # 提交队列任务
        # index,threadQueue,chapterName,chapterUrl
        priority = args[0]
        thread_queue = args[1]
        chapter_name = args[2]
        chapter_url = args[3]
        thread_queue.put(
            Content(priority=priority, chapterUrl=chapter_url, chapterName=chapter_name, whichRule=self.whichRule))
        log.info(f"提交,标题：{chapter_name},第 {priority} 个")
        time_sleep(self.downloadTaskDelayTime)
        return priority

    @staticmethod
    def getProcessNums() -> int:
        userSql = User.UserSql()
        result = userSql.selectProcessNums()
        log.info(f"调用的检索数据库中的进程数量: {str(result)}, {type(result)}")
        return result + 1

    def setDownloadTaskDelayTime(self) -> None:
        user_sql = User.UserSql()
        self.downloadTaskDelayTime = user_sql.selectDownloadTaskDelayTime() - 1

    @staticmethod
    def updateSqlDownloadInfo(taskfinishtime: str,
                              taskprogress: int,
                              taskstatusinfo: str,
                              taskbtnstatus: int,
                              taskserialNumber: int,
                              taskprogresslabel: int):  # 更新下载界面信息
        user_sql = User.UserSql()
        user_sql.updateDownloadInfo(taskfinishtime=taskfinishtime, taskprogress=taskprogress,
                                    taskstatusinfo=taskstatusinfo, taskbtnstatus=taskbtnstatus,
                                    taskserialNumber=taskserialNumber, taskprogresslabel=taskprogresslabel)

    @staticmethod
    def getSaveFileLocation() -> str:
        user_sql = User.UserSql()
        result = user_sql.selectSaveFileLocation()
        log.info(f"调用的检索数据库中的保存文件路径:{str(result)}, {type(result)}")
        if not os.path.exists(result):
            log.info("文件夹不存在，创建！")
            os.mkdir(result)
        return result

    @staticmethod
    def getRule() -> list:  # 获取用户自定义规则
        local_json = regular.Json()
        return local_json.getData()

    def getProgressValue(self) -> int:  # 获取进度
        return self.probar.value()

    def setLabelProbarProgress(self, info: int) -> None:  # 设置进度信息
        self.lb_probar.setText(f"{info}%")

    def setLabelProbarState(self, info: str) -> None:  # 设置文件状态信息
        self.labelProgressState.setText(info)

    def setProgressValue(self, value: int) -> None:  # 改变进度
        self.probar.setValue(value)

    def setBtnEnabled(self) -> None:  # 改变按钮可点击状态
        self.btnAddBookToBookShelf.setEnabled(True)
        self.btnFile.setEnabled(True)
        self.btnDel.setEnabled(True)

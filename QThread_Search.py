# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal, QFileInfo
import User
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from mock_useragent import UserAgent
from time import sleep as time_sleep
from queue import PriorityQueue
from concurrent.futures import ThreadPoolExecutor, as_completed
from search import Search
from log import Logger
import winreg

log = Logger().getlog()


class QThread_Search(QThread):
    breakSignal_addSearchResult = pyqtSignal(str, str, str, str, int, str, str, str, str, str, str, float, float, int,int)
    breakSignal_NoneSearch = pyqtSignal(str)
    breakSignal_int_showSearchNums = pyqtSignal(str)
    breakSignal_str_hideLodingGif = pyqtSignal(str)

    def __init__(self, searchText: str, rule: list):  # 搜索名字，规则
        super().__init__()
        self.searchText = searchText
        self.rule = rule
        self.search_process_nums = self.setSearchProcessNums()
        self.proxy_server = None
        self.setRequestProxyServer()

    def getComboboxIndex(self) -> int:
        user = User.UserSql()
        index = user.selectComboboxSortChooseIndex()
        return index

    def PutQueue(self, args: list) -> None:  # 提交队列任务
        # index,threadQueue,searchName_
        priority = args[0]
        thread_queue = args[1]
        rule = args[2]
        num = args[3]
        homeUrl = args[4]
        thread_queue.put(
            Search(priority=priority, searchName_=self.searchText, rule=rule, num=num,homeUrl=homeUrl))
        log.info(f"提交,搜索,第{num}个规则")
        return priority

    def getLocalProxyServer(self) -> tuple or None:  # 获取本机代理
        internet_setting = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
        handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, internet_setting, 0,
                                (winreg.KEY_WOW64_64KEY + winreg.KEY_READ))
        try:
            proxyServer = winreg.QueryValueEx(handle, "ProxyServer")[0]
            proxyEnable = winreg.QueryValueEx(handle, "ProxyEnable")[0]
            return proxyServer, int(proxyEnable)
        except FileNotFoundError:
            return None

    def setRequestProxyServer(self):
        proxy_server = self.getLocalProxyServer()
        if proxy_server is None:
            log.info("本机当前没有设置代理")
        elif proxy_server[1] == 0:
            log.info("本机当前未启用代理")
        else:
            self.proxy_server = {"http": proxy_server[0], "https": proxy_server[0]}
            log.info(f"本机当前代理:{proxy_server[0]}")

    def requestBookImage(self, url: str, image_name: str) -> str:
        image_name_path = QFileInfo("./Resource/Cache").absoluteFilePath()+f"/{image_name}"
        is_image = QFileInfo("./Resource/noCover.jpeg").absoluteFilePath()
        timeout_mistake = 0
        proxy_mistake = 0
        connection_mistake = 0
        while (timeout_mistake <= 2) and (proxy_mistake <= 2) and (connection_mistake <= 2):
            try:
                if self.proxy_server is None:
                    image_b = requests.get(url, headers={"User-Agent": UserAgent().random_chrome},
                                           timeout=10, verify=False)
                else:
                    image_b = requests.get(url, headers={"User-Agent": UserAgent().random_chrome},
                                           proxies=self.proxy_server,
                                           timeout=10, verify=False)
                if "image/jpeg" in image_b.headers["Content-Type"]:
                    image_bytes = image_b.content
                    with open(image_name_path, "wb") as f:
                        f.write(image_bytes)
                    image_b.close()
                    time_sleep(0.8)
                    is_image = QFileInfo(f"./Resource/Cache/{image_name}").absoluteFilePath()
                else:
                    log.warning("该链接不是图片")
                break
            except requests.Timeout:
                timeout_mistake += 1
                log.warning(f"当前连接超时第{timeout_mistake}次，下载图片失败")
                time_sleep(2)
            except requests.exceptions.ProxyError:
                proxy_mistake += 1
                self.proxy_server = {"http": None, "https": None}
                log.error(f"本机代理请求图片资源错误第{proxy_mistake}次,不启用本机代理")
                time_sleep(0.5)
            except requests.exceptions.ConnectionError:
                connection_mistake += 1
                log.error(f"request的连接数过多 或 请求速度过快，当前第{connection_mistake}次错误")
                time_sleep(2)

        return is_image

    @staticmethod
    def setSearchProcessNums():
        user = User.UserSql()
        return user.selectUserInfo()["searchProcessNum"]

    @staticmethod
    def getIsDownload() -> list:
        user = User.UserSql()
        urlList = [url[0] for url in user.selectHomeUrl()]
        return urlList

    def run(self) -> None:
        thread_queue = PriorityQueue()  # 线程队列
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.adapters.DEFAULT_RETRIES = 5
        homeUrl = self.getIsDownload()
        with ThreadPoolExecutor(max_workers=self.search_process_nums) as t:
            task_out_queue = []
            search_to_index = 0
            for i in range(len(self.rule)):
                if self.rule[i]["enable"] == 2:
                    log.info(f"规则{self.rule[i]['bookSourceName']}搜索")
                    sub_args = (search_to_index, thread_queue, self.rule[i], i,homeUrl)
                    task = t.submit(self.PutQueue, sub_args)
                    search_to_index += 1
                    task_out_queue.append(task)
                    time_sleep(0.5)
            for queue in as_completed(task_out_queue):
                queue.result()
            searchNums = 0
            combobox_index = self.getComboboxIndex()
            self.breakSignal_str_hideLodingGif.emit("")  # 发送隐藏loding的gif信号
            while not thread_queue.empty():
                get_queue = thread_queue.get()
                log.info(f"取出搜索结果{str(get_queue.search_reult_list)}")
                for search_list in get_queue.search_reult_list:
                    searchNums += 1
                    image = search_list["image"]
                    search_list["content"] = search_list["content"][0:123] + "......" if len(
                        search_list["content"]) > 126 else search_list["content"]
                    bookname = search_list['bookname']
                    author = search_list["author"]
                    if self.searchText in bookname:
                        bookname = bookname.replace(self.searchText, f'<font color="#F30">{self.searchText}</font>')
                    if self.searchText in author:
                        author = author.replace(self.searchText, f'<font color="#F30">{self.searchText}</font>')
                    content = f'''
                                <li>书名：
                                    <span>{bookname}</span>
                                </li>
                                <li>作者：
                                    <span>{author}</span>
                                </li>
                                <li>状态：
                                    <span>{search_list["endstate"]}</span>
                                </li>
                                <li>最新章节：
                                    <span>{search_list["latestChapter"]}</span>
                                </li>
                                <li>更新时间：
                                    <span>{search_list["updateTime"]}</span>
                                </li>
                                <li>简介：
                                    <span>{search_list["content"]}</span>
                                </li>
                                <li>源：
                                    <span>{search_list["source"]}</span>
                                </li>'''
                    url = search_list["url"]
                    whichRule = int(search_list["whichRule"])
                    image_name = image.replace(":", "_").replace("/", "_")
                    # path = os.getcwd().replace("\\", "/") + "/Resource/Cache/" + image_name
                    path = QFileInfo("./Resource/Cache").absoluteFilePath()+f"/{image_name}"
                    log.info(f"图片路径：{path}")
                    log.info(f"图片：{image}")
                    if image:
                        if os.path.isfile(path) is False:
                            log.info(f"文件不存在，下载图片:{image}")
                            path = self.requestBookImage(url=image, image_name=image_name)
                        else:
                            log.info("图片本地缓存存在，无需下载")
                    else:
                        # path = os.getcwd().replace("\\", "/") + "/Resource/noCover.jpeg"
                        path = QFileInfo("./Resource/noCover.jpeg").absoluteFilePath()
                    log.info(path)
                    self.breakSignal_addSearchResult.emit(
                        path,
                        search_list['bookname'],
                        content,
                        url,
                        whichRule,
                        author,
                        search_list['endstate'],
                        search_list['source'],
                        search_list['latestChapter'],
                        search_list['updateTime'],
                        search_list['content'],
                        search_list['bookname_similarity'],
                        search_list['author_similarity'],
                        combobox_index,
                        search_list["isDownload"]
                    )  # 发送添加搜索结果的信号
                    self.breakSignal_int_showSearchNums.emit(
                        f'"{self.searchText}"的搜索结果: {searchNums} 个')  # 发送搜索到的结果label修改text信号
                    time_sleep(0.3)
                    # time.sleep(0.3)
            if not searchNums:
                self.breakSignal_NoneSearch.emit("")  # 发送没有搜索结果的信号

        return
        # try:
        #     search_ = Search(self.searchText, self.rule)
        #     search_list = search_.getSearchResult()
        #     # log.info(search_list)
        #     # # 测试使用
        #     combobox_index = self.getComboboxIndex()
        #     # 需传入：图片地址 简介 主页目录地址 第N个规则
        #     self.breakSignal_str_hideLodingGif.emit("")  # 发送隐藏loding的gif信号
        #     searchNums = 0
        #     for i in search_list:
        #         log.info(str(i))
        #         searchNums += 1
        #         image = i["image"]
        #         i["content"] = i["content"][0:123] + "......" if len(i["content"]) > 126 else i["content"]
        #         bookname = i['bookname']
        #         author = i["author"]
        #         if self.searchText in bookname:
        #             bookname = bookname.replace(self.searchText, f'<font color="#F30">{self.searchText}</font>')
        #             # <font color="#F30">{i['bookname']}</font>
        #         if self.searchText in author:
        #             author = author.replace(self.searchText, f'<font color="#F30">{self.searchText}</font>')
        #         content = f'''
        #                     <li>书名：
        #                         <span>{bookname}</span>
        #                     </li>
        #                     <li>作者：
        #                         <span>{author}</span>
        #                     </li>
        #                     <li>状态：
        #                         <span>{i["endstate"]}</span>
        #                     </li>
        #                     <li>最新章节：
        #                         <span>{i["latestChapter"]}</span>
        #                     </li>
        #                     <li>更新时间：
        #                         <span>{i["updateTime"]}</span>
        #                     </li>
        #                     <li>简介：
        #                         <span>{i["content"]}</span>
        #                     </li>
        #                     <li>源：
        #                         <span>{i["source"]}</span>
        #                     </li>'''
        #         url = i["url"]
        #         whichRule = int(i["whichRule"])
        #         image_name = image.replace(":", "_").replace("/", "_")
        #         path = os.getcwd().replace("\\", "/") + "/Resource/Cache/" + image_name
        #         log.info(f"图片路径：{path}")
        #         log.info(f"图片：{image}")
        #         if image:
        #             if os.path.isfile(path) is False:
        #                 log.info("文件不存在，下载图片:{image}")
        #                 try:
        #                     image_bytes = requests.get(image, timeout=3,verify = False).content
        #                     with open(path, "wb") as f:
        #                         f.write(image_bytes)
        #                 except Exception:
        #                     log.info("下载图片失败")
        #                     path = os.getcwd().replace("\\", "/") + "/Resource/noCover.jpeg"
        #         else:
        #             path = os.getcwd().replace("\\", "/") + "/Resource/noCover.jpeg"
        #         self.breakSignal_addSearchResult.emit(
        #             path,
        #             i['bookname'],
        #             content,
        #             url,
        #             whichRule,
        #             author,
        #             i['endstate'],
        #             i['source'],
        #             i['latestChapter'],
        #             i['updateTime'],
        #             i['content'],
        #             i['bookname_similarity'],
        #             i['author_similarity'],
        #             combobox_index
        #         )  # 发送添加搜索结果的信号
        #         self.breakSignal_int_showSearchNums.emit(
        #             f'"{self.searchText}"的搜索结果: {searchNums} 个')  # 发送搜索到的结果label修改text信号
        #         time_sleep(0.3)
        #         # time.sleep(0.3)
        #     if not search_list:
        #         self.breakSignal_NoneSearch.emit("")  # 发送没有搜索结果的信号
        #     # self.breakSignal_int_showSearchNums.emit(f"当前搜索到的结果为：{len(search_list)} 个")  # 发送搜索到的结果label修改text信号
        #
        # except Exception as err:
        #     # self.breakSignal_str_hideLodingGif.emit("")  # 发送隐藏loding的gif信号
        #     log.error(err)
        # self.breakSignal_hideReflushIcon.emit('')
        # self.breakSignal_addVSpacer.emit("")

# -*- coding: utf-8 -*-
import requests
from mock_useragent import UserAgent
from lxml import etree
from difflib import SequenceMatcher
from log import Logger

log = Logger().getlog()


class Search:
    def __init__(self, searchName_: str, priority: int, rule: dict, num: int,homeUrl:list):
        self.priority = priority
        self.searchName_ = searchName_  # 用户搜索名字
        self.rule = rule  # 读取的本地json规则
        self.num = num
        self.hashomeUrl = homeUrl
        self.getSearchResult()

    def __lt__(self, other):
        return self.priority < other.priority

    def encode(self, rule: dict):  # 获取搜索名字编码
        charset = str(rule["charset"])
        newSearchName = str(self.searchName_.encode(charset))
        return newSearchName.replace("\\x", "%").replace("b'", "").replace("'", "")

    @staticmethod
    def __string_similar(str_1: str, str_2: str) -> float:  # 获取相似度
        return round(SequenceMatcher(None, str_1, str_2).quick_ratio(), 3)

    def getSearchResult(self) -> None:
        self.search_reult_list = []
        try:
            bookSourceUrl = self.rule["bookSourceUrl"]
            bookSourceName = self.rule["bookSourceName"]
            searchUrl: str = bookSourceUrl + self.rule["searchUrl"]
            searchName_coding = self.encode(self.rule)  # 将搜索名字进行编码
            headers = {
                "User-Agent": UserAgent().random_chrome,
                "Referer": self.rule["bookSourceUrl"] + "/",
            }
            charset = self.rule["charset"]  # 编码
            if str(self.rule["method"]) == "1":  # 1是get 2是post
                log.info(f"规则{self.num}:"+searchUrl + searchName_coding)
                searchUrl = searchUrl.replace("f'{searchName_}'", f"{searchName_coding}")
                response = requests.get(url=searchUrl, headers=headers, verify=False)
            else:
                data = self.rule["data"]
                data = data.replace("f'{searchName_}'", f"{searchName_coding}")
                headers.update({"Content-Type": "application/x-www-form-urlencoded"})
                response = requests.post(url=searchUrl, headers=headers, data=data, verify=False)

            response_decode = response.content.decode(charset, "ignore")
            html_list_2 = self.__getLxml_search(response_decode, bookSourceName, bookSourceUrl, self.rule, self.num,
                                                response.url)
            if not html_list_2: log.info(f"规则{self.num}:没有数据")
            self.search_reult_list.extend(html_list_2)
        except etree.XPathEvalError:
            log.warning(f"规则{self.num}:xpath解析错误,不添加进数组")
            self.search_reult_list = []

    def parseElement(self, html_list, element, source, num, rule, bookSourceUrl) -> list:
        for i in element:
            html_dict = {
                "url": "",
                "image": "",
                "bookname": "",
                "author": "",
                "endstate": "",
                "latestChapter": "",
                "updateTime": "",
                "content": "",
                "source": source,
                "whichRule": num,
                "bookname_similarity": "",
                "author_similarity": "",
                "isDownload": 0
            }
            html_url = i.xpath(rule["searchBook"]["toUrl"]) if rule["searchBook"]["toUrl"] else []  # 主页地址
            html_img = i.xpath(rule["searchBook"]["image"]) if rule["searchBook"]["image"] else []  # 图片地址
            html_bookname = i.xpath(rule["searchBook"]["bookname"]) if rule["searchBook"]["bookname"] else []  # 标题
            html_author = i.xpath(rule["searchBook"]["author"]) if rule["searchBook"]["author"] else []  # 作者
            html_EndState = i.xpath(rule["searchBook"]["endstate"]) if rule["searchBook"]["endstate"] else []  # 完结状态
            html_latestChapter = i.xpath(rule["searchBook"]["latestChapter"]) if rule["searchBook"][
                "latestChapter"] else []  # 最新章节
            html_updateTime = i.xpath(rule["searchBook"]["updateTime"]) if rule["searchBook"][
                "updateTime"] else []  # 更新时间
            html_content = i.xpath(rule["searchBook"]["content"]) if rule["searchBook"]["content"] else []  # 简介

            html_dict["url"] = html_url[0] if html_url else ""

            if html_url and ("http" not in html_url[0]):
                html_dict["url"] = bookSourceUrl + html_dict["url"]
            html_dict["image"] = html_img[0] if html_img else ""
            if html_img and ("http" not in html_dict["image"]):
                if html_dict["image"][0] != '/':
                    html_dict["image"] = '/'+html_dict["image"]
                    log.info(html_dict["image"])
                html_dict["image"] = bookSourceUrl + html_dict["image"]
            else:
                html_dict["image"] = html_dict["image"]
            for name in html_bookname: html_dict["bookname"] += name
            for author in html_author: html_dict["author"] += author
            for endstate in html_EndState: html_dict["endstate"] += endstate
            for latestChapter in html_latestChapter: html_dict["latestChapter"] += latestChapter
            for updateTime in html_updateTime: html_dict["updateTime"] += updateTime
            for content in html_content: html_dict["content"] += content
            html_dict["bookname_similarity"] = self.__string_similar(str_1=self.searchName_,
                                                                     str_2=html_dict["bookname"])
            html_dict["author_similarity"] = self.__string_similar(str_1=self.searchName_, str_2=html_dict["author"])

            if html_dict["url"] in self.hashomeUrl:
                html_dict["isDownload"] = 1
            html_list.append(html_dict)
        return html_list

    def parseElementOnly(self, html_list, html, source, num, rule, bookSourceUrl, resp_url) -> list:
        html_dict = {
            "url": "",
            "image": "",
            "bookname": "",
            "author": "",
            "endstate": "",
            "latestChapter": "",
            "updateTime": "",
            "content": "",
            "source": source,
            "whichRule": num,
            "bookname_similarity": "",
            "author_similarity": "",
            "isDownload": 0
        }
        html_url_rule = rule["searchBook"]["onlySearch"]["toUrl"]  # 主页地址
        html_img = html.xpath(rule["searchBook"]["onlySearch"]["image"]) if rule["searchBook"]["onlySearch"][
            "image"] else []  # 图片地址
        html_bookname = html.xpath(rule["searchBook"]["onlySearch"]["bookname"]) if rule["searchBook"]["onlySearch"][
            "bookname"] else []  # 标题
        html_author = html.xpath(rule["searchBook"]["onlySearch"]["author"]) if rule["searchBook"]["onlySearch"][
            "author"] else []  # 作者
        html_EndState = html.xpath(rule["searchBook"]["onlySearch"]["endstate"]) if rule["searchBook"]["onlySearch"][
            "endstate"] else []  # 完结状态
        html_latestChapter = html.xpath(rule["searchBook"]["onlySearch"]["latestChapter"]) if \
            rule["searchBook"]["onlySearch"]["latestChapter"] else []  # 最新章节
        html_updateTime = html.xpath(rule["searchBook"]["onlySearch"]["updateTime"]) if \
            rule["searchBook"]["onlySearch"]["updateTime"] else []  # 更新时间
        html_content = html.xpath(rule["searchBook"]["onlySearch"]["content"]) if rule["searchBook"]["onlySearch"][
            "content"] else []  # 简介

        html_dict["url"] = resp_url if html_url_rule == "{resp_url}" else html.xpath(html_url_rule)[0]
        if "http" not in html_dict["url"]:
            html_dict["url"] = bookSourceUrl + html_dict["url"]
        html_dict["image"] = html_img[0] if html_img else ""
        if "http" not in html_dict["image"]:
            if html_dict["image"][0] != "/":
                html_dict["image"] = "/"+html_dict["image"]
            html_dict["image"] = bookSourceUrl + html_dict["image"]
        else:
            html_dict["image"] = html_dict["image"]
        for name in html_bookname: html_dict["bookname"] += name
        for author in html_author: html_dict["author"] += author
        for endstate in html_EndState: html_dict["endstate"] += endstate
        for latestChapter in html_latestChapter: html_dict["latestChapter"] += latestChapter
        for updateTime in html_updateTime: html_dict["updateTime"] += updateTime
        for content in html_content: html_dict["content"] += content
        html_dict["bookname_similarity"] = self.__string_similar(str_1=self.searchName_, str_2=html_dict["bookname"])
        html_dict["author_similarity"] = self.__string_similar(str_1=self.searchName_, str_2=html_dict["author"])

        if html_dict["url"] in self.hashomeUrl:
            html_dict["isDownload"] = 1
        html_list.append(html_dict)
        return html_list

    # params:
    #       resp  ==>  获取的网页text
    #       source   ==>  搜索源
    #       bookSourceUrl   ==>  搜索源的地址
    #       rule   ==>  用户规则
    def __getLxml_search(self, resp, source, bookSourceUrl, rule, num, resp_url) -> list:
        try:
            html = etree.HTML(resp)
            html_list = []
            noneSearch = rule["searchBook"]["noneSearch"]  # 空结果规则必须特定唯一
            element = html.xpath(rule["searchBook"]["element"]) if rule["searchBook"]["element"] else []  # 解析的节点
            isOnlySearch = rule["searchBook"]["onlySearch"]["isOnlySearch"]
            elementOnly = html.xpath(rule["searchBook"]["onlySearch"]["element"]) if rule["searchBook"]["onlySearch"][
                "element"] else []  # 解析的单一搜索结果节点
            if noneSearch and html.xpath(noneSearch):  # 如果规则存在
                log.info(f"规则{self.num}:该规则有特定空规则并已匹配到空结果，返回空列表")
                return html_list  # 匹配到空结果
            if element:  # 判断搜索结果解析的是否为空
                log.info(f"规则{self.num}:xpath解析有结果")
                html_list = self.parseElement(html_list, element, source, num, rule, bookSourceUrl)
                return html_list
            if isOnlySearch and elementOnly:
                log.info(f"规则{self.num}:xpath解析搜索结果为空,但是搜索到为单一结果")
                html_list = self.parseElementOnly(html_list, html, source, num, rule, bookSourceUrl, resp_url)
                return html_list
            return html_list
        except AttributeError:
            log.error(f"规则{self.num}:lxml解析失败")
            return []

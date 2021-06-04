# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QThread
from time import sleep as time_sleep, time as time_time, strftime as time_strftime, gmtime as time_gmtime
from markdown2 import markdown
from mock_useragent import UserAgent
from lxml import etree
import regular, requests
import re
from log import Logger
log = Logger().getlog()
class QThread_Debug(QThread):
    breakSignal_setDebugMarkdownResult = pyqtSignal(str)
    breakSignal_setDebugingRefreshIconStatus = pyqtSignal(bool)

    def __init__(self, debug_searchName: str, whichRule: int):
        super().__init__()
        self.debug_searchName = debug_searchName
        self.noRule = "whitesev"
        self.rule = regular.Json().getData()[whichRule]  # 初始化当前需要调试得到自定义规则
        self.start_time = time_time()

    def run(self):
        self.breakSignal_setDebugingRefreshIconStatus.emit(True)
        log.info(str(self.rule))
        self.sendHTML(s=f"{self.getTime()}⇒当前启动的规则:{self.rule['bookSourceName']}")
        status = self.Searh() and self.Catalog() and self.Content()
        if status is False:
            self.sendHTML(s=f"<br>{self.getTime()}⇒调试中断")  # 调试中断
        else:
            self.sendHTML(s=f"<br>{self.getTime()}⇒调试完毕")
        self.breakSignal_setDebugingRefreshIconStatus.emit(False)

    def Searh(self):
        self.sendHTML("<br>")
        self.sendHTML(s=f"## 搜索")
        if self.debug_searchName.strip():
            self.sendHTML(s=f"<br>{self.getTime()}⇒开始搜索关键字:{self.debug_searchName}")
        else:
            self.sendHTML(s=f"<br>{self.getTime()}⇒开始搜索关键字:null")
            return False
        self.sendHTML(s=f"<br>{self.getTime()}︾开始解析搜索页")
        bookSourceUrl = self.rule["bookSourceUrl"]
        searchUrl: str = bookSourceUrl + self.rule["searchUrl"]
        searchName_coding = self.Search_encode()  # 将搜索名字进行编码
        headers = {
            "User-Agent": UserAgent().random_chrome,
            "Referer": self.rule["bookSourceUrl"] + "/",
        }
        self.sendHTML(s=f"<br>{self.getTime()} ┌获取请求方法")
        if str(self.rule["method"]) == "1":  # 1是get 2是post
            self.sendHTML(s=f"<br>{self.getTime()} └GET")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取请求链接")
            searchUrl = searchUrl.replace("f'{searchName_}'", f"{searchName_coding}")
            response = requests.get(url=searchUrl, headers=headers,verify=False)
            self.sendHTML(s=f"<br>{self.getTime()} └[{searchUrl}]({searchUrl})")

        else:
            self.sendHTML(s=f"<br>{self.getTime()} └POST")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取请求链接")
            self.sendHTML(s=f"<br>{self.getTime()} └[{searchUrl}]({searchUrl})")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取请求data")
            data = self.rule["data"]
            data = data.replace("f'{searchName_}'", f"{searchName_coding}")
            self.sendHTML(s=f"<br>{self.getTime()} └{data}")
            headers.update({"Content-Type": "application/x-www-form-urlencoded"})
            response = requests.post(url=searchUrl, headers=headers, data=data,verify=False)


        response_decode = response.content.decode(self.rule["charset"], "ignore")
        html_list = self.Search_getLxml_search(resp=response_decode)

        if html_list is None:
            return False
        else:
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取封面链接")
            self.sendHTML(s=f"<br>{self.getTime()} └[{html_list[0]['image']}]({html_list[0]['image']})")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取详情页链接")
            self.sendHTML(s=f"<br>{self.getTime()} └[{html_list[0]['toUrl']}]({html_list[0]['toUrl']})")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取更新状态")
            self.sendHTML(s=f"<br>{self.getTime()} └{html_list[0]['endstate']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取书名")
            self.sendHTML(s=f"<br>{self.getTime()} └{html_list[0]['bookname']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取作者")
            self.sendHTML(s=f"<br>{self.getTime()} └{html_list[0]['author']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取更新状态")
            self.sendHTML(s=f"<br>{self.getTime()} └{html_list[0]['endstate']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取最新章节")
            self.sendHTML(s=f"<br>{self.getTime()} └{html_list[0]['latestChapter']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取更新时间")
            self.sendHTML(s=f"<br>{self.getTime()} └{html_list[0]['updateTime']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取简介")
            self.sendHTML(s=f"<br>{self.getTime()} └{html_list[0]['content']}")
            self.Search_toUrl = html_list[0]["toUrl"]
            self.Search_toUrl = self.Search_toUrl if "http" in self.Search_toUrl else self.rule["bookSourceUrl"]+self.Search_toUrl
        self.sendHTML(s=f"<br>{self.getTime()}︽搜索页解析完成")
        return True

    def Search_encode(self) -> str:  # 获取搜索名字编码
        charset = str(self.rule["charset"])
        newSearchName = str(self.debug_searchName.encode(charset))
        return newSearchName.replace("\\x", "%").replace("b'", "").replace("'", "")
    def Search_getLxml_search(self, resp:str) -> list:
        self.sendHTML(s=f"<br>{self.getTime()} ┌获取书籍列表")
        html = etree.HTML(resp)
        isOnlySearch = self.rule["searchBook"]["onlySearch"]["isOnlySearch"]
        try:
            element = html.xpath(self.rule["searchBook"]["element"] or self.noRule)# 解析的节点
            element_only = html.xpath(self.rule["searchBook"]["onlySearch"]["element"] or self.noRule)
            noneSearch = html.xpath(self.rule["searchBook"]["noneSearch"] or self.noRule)
        except etree.XPathEvalError:
            self.sendHTML(s=f"<br>{self.getTime()} └语法错误")
            return None
        print(html.xpath(self.rule["searchBook"]["element"]))
        if noneSearch:  # 如果规则存在
            log.info("debug:该规则有特定空规则并已匹配到空结果，返回空列表")
            self.sendHTML(s=f"<br>{self.getTime()} └null")
            return None  # 匹配到空结果

        if element:  # 判断搜索结果解析的是否为空
            log.info("xpath解析有结果")
            html_list_parse = self.Search_parseElement(element=element)
            if html_list_parse:
                self.sendHTML(s=f"<br>{self.getTime()} └列表大小:{len(html_list_parse)}")
                if len(html_list_parse) ==0:
                    return None
            else:
                self.sendHTML(s=f"<br>{self.getTime()} └null")
            return html_list_parse

        if isOnlySearch and element_only:
            log.info("xpath解析搜索结果为空,但是搜索到为单一结果")
            html_list_parse_only = self.Search_parseElementOnly(element=element_only)
            if html_list_parse_only:
                self.sendHTML(s=f"<br>{self.getTime()} └列表大小:0 单一结果")
            else:
                self.sendHTML(s=f"<br>{self.getTime()} └null")
            return html_list_parse_only
        self.sendHTML(s=f"<br>{self.getTime()} └null")
        return None
    def Search_parseElement(self,element:etree._Element)->list:
        html_list = []
        for i in element:
            html_dict = {
                "toUrl": "",
                "image": "",
                "bookname": "",
                "author": "",
                "endstate": "",
                "latestChapter": "",
                "updateTime": "",
                "content": ""
            }
            try:
                for toUrl in i.xpath(self.rule["searchBook"]["toUrl"] or self.noRule):
                    html_dict["toUrl"] += toUrl
                for image in i.xpath(self.rule["searchBook"]["image"] or self.noRule):
                    html_dict["image"] += image
                for bookname in i.xpath(self.rule["searchBook"]["bookname"] or self.noRule):
                    html_dict["bookname"] += bookname
                for author in i.xpath(self.rule["searchBook"]["author"] or self.noRule):
                    html_dict["author"] += author
                for endstate in i.xpath(self.rule["searchBook"]["endstate"] or self.noRule):
                    html_dict["endstate"] += endstate
                for latestChapter in i.xpath(self.rule["searchBook"]["latestChapter"] or self.noRule):
                    html_dict["latestChapter"] += latestChapter
                for updateTime in i.xpath(self.rule["searchBook"]["updateTime"] or self.noRule):
                    html_dict["updateTime"] += updateTime
                for content in i.xpath(self.rule["searchBook"]["content"] or self.noRule):
                    html_dict["content"] += content
                html_list.append(html_dict)
            except etree.XPathEvalError:
                self.sendHTML(s=f"<br>{self.getTime()} └语法错误")
                return None

        return html_list if html_list else None
    def Search_parseElementOnly(self,element:etree._Element)->list:
        html_list = []
        html_dict = {
            "toUrl": "",
            "image": "",
            "bookname": "",
            "author": "",
            "endstate": "",
            "latestChapter": "",
            "updateTime": "",
            "content": "",
        }
        try:
            for toUrl in i.xpath(self.rule["searchBook"]["onlySearch"]["toUrl"] or self.noRule):
                html_dict["toUrl"] += toUrl
            for image in i.xpath(self.rule["searchBook"]["onlySearch"]["image"] or self.noRule):
                html_dict["image"] += image
            for bookname in i.xpath(self.rule["searchBook"]["onlySearch"]["bookname"] or self.noRule):
                html_dict["bookname"] += bookname
            for author in i.xpath(self.rule["searchBook"]["onlySearch"]["author"] or self.noRule):
                html_dict["author"] += author
            for endstate in i.xpath(self.rule["searchBook"]["onlySearch"]["endstate"] or self.noRule):
                html_dict["endstate"] += endstate
            for latestChapter in i.xpath(self.rule["searchBook"]["onlySearch"]["latestChapter"] or self.noRule):
                html_dict["latestChapter"] += latestChapter
            for updateTime in i.xpath(self.rule["searchBook"]["onlySearch"]["updateTime"] or self.noRule):
                html_dict["updateTime"] += updateTime
            for content in i.xpath(self.rule["searchBook"]["onlySearch"]["content"] or self.noRule):
                html_dict["content"] += content
            html_list.append(html_dict)
            return html_list if html_dict["toUrl"] else None
        except etree.XPathEvalError:
            log.info("xpath语法错误")
            return None

    def Catalog(self):
        self.sendHTML("<br>")
        self.sendHTML(s=f"## 目录")
        self.sendHTML(s=f"<br>{self.getTime()}︾开始解析目录页")
        self.sendHTML(s=f"<br>{self.getTime()} ≡当前详情页:[{self.Search_toUrl}]({self.Search_toUrl})")

        bookid = re.findall(r"\d+\d*", self.Search_toUrl)
        self.sendHTML(s=f"<br>{self.getTime()} ┌获取当前id")
        self.sendHTML(s=f"<br>{self.getTime()} └{bookid}")
        self.sendHTML(s=f"<br>{self.getTime()} ┌获取启用模式")
        model = self.rule["catalog"]["model"]
        if model==1:
            self.sendHTML(s=f"<br>{self.getTime()} └模式1")
            contentsPageResp = self.Catalog_getContentsPageResp()
            if not contentsPageResp: return False
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取目录列表")
            chapterUrl = self.Catalog_getChapterUrl(url=self.Search_toUrl)
            if len(chapterUrl) == 0: return False
            self.sendHTML(s=f"<br>{self.getTime()} └列表大小{len(chapterUrl)}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌首章名称")
            self.sendHTML(s=f"<br>{self.getTime()} └{chapterUrl[0]['chapterName']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌首章链接")
            self.sendHTML(s=f"<br>{self.getTime()} └{chapterUrl[0]['bookUrl']}")
            self.Catalog_Url = chapterUrl[0]['bookUrl']
        elif model==2:
            self.sendHTML(s=f"<br>{self.getTime()} └模式2")
            self.sendHTML(s=f"<br>{self.getTime()} ┌当前目录页")
            contentsPageResp = self.Catalog_getContentsPageResp()
            if not contentsPageResp: return False
            catalog_url = self.Catalog_getCatalogUrl(resp=contentsPageResp)
            if not catalog_url: return False
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取目录列表")
            chapterUrl = self.Catalog_getChapterUrl(url = catalog_url)
            if len(chapterUrl) == 0:return False
            self.sendHTML(s=f"<br>{self.getTime()} └列表大小{len(chapterUrl)}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌首章名称")
            self.sendHTML(s=f"<br>{self.getTime()} └{chapterUrl[0]['chapterName']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌首章链接")
            self.sendHTML(s=f"<br>{self.getTime()} └{chapterUrl[0]['bookUrl']}")
            self.Catalog_Url = chapterUrl[0]['bookUrl']

        elif model == 3:
            self.sendHTML(s=f"<br>{self.getTime()} └模式3")
        elif model == 4:
            self.sendHTML(s=f"<br>{self.getTime()} └模式4")
            self.sendHTML(s=f"<br>{self.getTime()} ┌当前目录页")
            contentsPageResp = self.Catalog_getContentsPageResp()
            if not contentsPageResp:return False
            catalog_url = self.Catalog_getCatalogUrl(resp=contentsPageResp)
            if not catalog_url:return False
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取目录列表")
            chapterUrl = self.Catalog_getChapterUrl(url = catalog_url)
            self.sendHTML(s=f"<br>{self.getTime()} └列表大小{len(chapterUrl)}")
            if len(chapterUrl) == 0 :return False
            self.sendHTML(s=f"<br>{self.getTime()} ┌首章名称")
            self.sendHTML(s=f"<br>{self.getTime()} └{chapterUrl[0]['chapterName']}")
            self.sendHTML(s=f"<br>{self.getTime()} ┌首章链接")
            self.sendHTML(s=f"<br>{self.getTime()} └[{chapterUrl[0]['bookUrl']}]({chapterUrl[0]['bookUrl']})")
            self.Catalog_Url = chapterUrl[0]['bookUrl']
        else:
            self.sendHTML(s=f"<br>{self.getTime()} └模式5")
            self.sendHTML(s=f"<br>{self.getTime()} ┌当前目录页")
            self.sendHTML(s=f"<br>{self.getTime()} └[{self.Search_toUrl}]({self.Search_toUrl})")
            self.sendHTML(s=f"<br>{self.getTime()} ┌获取目录列表")
            chaptetLists = self.Catalog_getPages_model_5()
            self.sendHTML(s=f"<br>{self.getTime()} └列表大小{len(chaptetLists)}")
            self.Catalog_Url = chaptetLists[0]['bookUrl']

        self.sendHTML(s=f"<br>{self.getTime()}︽目录页解析完成")
        return True
    def Catalog_getNextPageUrl(self,resp:str)->str:
        html = etree.HTML(resp)
        try:
            nextPage = html.xpath(self.rule["catalog"]["nextPage"])[0] if html.xpath(self.rule["catalog"]["nextPage"] or self.noRule) else ""
            if nextPage:
                return nextPage
            else:
                return None
        except etree.XPathEvalError:
            self.sendHTML(s=f"<br>{self.getTime()} └语法错误")
            return None

    def Catalog_getPages_model_5(self): #获取各个章节(翻页)
        flag = True
        chapterList = []
        while True:
            chapterList.extend(self.Catalog_getChapterUrl(url=self.Search_toUrl))
            nowUrlResp = self.Catalog_getContentsPageResp()
            if nowUrlResp is None:
                flag = False
                break
            nextPageUrl = self.Catalog_getNextPageUrl(resp=nowUrlResp)
            if nextPageUrl is None:
                flag = False
                break
            self.Search_toUrl = nextPageUrl if "http" in nextPageUrl else self.rule["bookSourceUrl"]+nextPageUrl
            log.info("下一页url%s"%self.Search_toUrl)
        if flag:
            return chapterList
        else:
            return []
    def Catalog_getContentsPageResp(self)->str:#获取目录详情页响应
        headers = {
            "User-Agent": UserAgent().random_chrome,
            "Referer": self.Search_toUrl
        }
        try:
            homeResp = requests.get(url=self.Search_toUrl, headers=headers,timeout=10,verify=False).content.decode(self.rule["charset"])
            return homeResp
        except requests.Timeout:
            log.error("debug:连接超时")
            self.sendHTML(s=f"<br>{self.getTime()} └连接超时")
            return None
    def Catalog_getCatalogUrl(self,resp:str)->str: #获取章节页的url
        html = etree.HTML(resp)
        try:
            catalog_url_su = html.xpath(self.rule["catalog"]["toUrl"])[0] if html.xpath(self.rule["catalog"]["toUrl"] or self.noRule) else ""
        except etree.XPathEvalError:
            self.sendHTML(s=f"<br>{self.getTime()} └语法错误")
            return None
        catalog_url = catalog_url_su if "http" in catalog_url_su else self.rule["bookSourceUrl"]+catalog_url_su
        log.info(catalog_url)
        self.sendHTML(s=f"<br>{self.getTime()} └[{catalog_url}]({catalog_url})")
        if catalog_url:
            return catalog_url
        else:
            return None
    def Catalog_getChapterUrl(self,url:str)->list: #获取目录列表
        headers = {
            "User-Agent": UserAgent().random_chrome,
            "Referer": self.Search_toUrl
        }
        try:
            catalog_resp = requests.get(url=url, headers=headers,timeout=10,verify=False).content.decode(self.rule["charset"])
        except requests.Timeout:
            log.warning("debug:获取目录列表超时")
            return []
        html = etree.HTML(catalog_resp)
        catalog_list = []
        try:
            for i in html.xpath(self.rule["catalog"]["element"] or self.noRule):
                catalog_dict = {
                    "bookUrl": "",
                    "chapterName": ""
                }
                bookurl = i.xpath(self.rule["catalog"]["bookUrl"] or self.noRule)
                chapterName = i.xpath(self.rule["catalog"]["chapterName"] or self.noRule)
                bookurl_new = bookurl[0] if bookurl else ""
                if bookurl_new and bookurl_new[0:4] != "http":
                    bookurl_new = self.rule["bookSourceUrl"] + bookurl_new
                catalog_dict["bookUrl"] = bookurl_new
                catalog_dict["chapterName"] = chapterName[0] if chapterName else ""
                log.info(str(catalog_dict))
                catalog_list.append(catalog_dict)
            return catalog_list
        except etree.XPathEvalError:
            self.sendHTML(s=f"<br>{self.getTime()} └语法错误")
            return []

    def Content(self):
        headers = {
            "User-Agent": UserAgent().random_chrome,
        }
        self.sendHTML("<br>")
        self.sendHTML(s=f"## 正文")
        self.sendHTML(s=f"<br>{self.getTime()}︾开始解析正文页")
        self.sendHTML(s=f"<br>{self.getTime()} ≡当前正文链接:[{self.Catalog_Url}]({self.Catalog_Url})")
        self.sendHTML(s=f"<br>{self.getTime()} ┌获取正文内容")
        try:
            resp = requests.get(url=self.Catalog_Url, headers=headers, timeout=10,verify=False).content.decode(self.rule["charset"])
            content = self.Content_ParseResult(resp)
            self.sendHTML(s=f"<br>{self.getTime()} └{content}")
        except requests.exceptions.Timeout:
            self.sendHTML(s=f"<br>{self.getTime()} └连接超时，获取失败")
            return False
        self.sendHTML(s=f"<br>{self.getTime()}︽正文页解析完成")
        return True
    def Content_ParseResult(self,resp:str)->str:
        html = etree.HTML(resp)
        content_text_list = html.xpath(self.rule["content"]["text"] or self.noRule)
        content_text = ""
        for content in content_text_list:
            content_text += content
        return content_text.strip()

    def sendHTML(self, s):
        extras = ['code-friendly', 'fenced-code-blocks', 'footnotes', 'tables', 'code-color', 'pyshell', 'nofollow',
                  'cuddled-lists', 'header ids', 'nofollow']
        markdown_html = markdown(s, extras=extras)
        log.info(str(markdown_html))
        self.breakSignal_setDebugMarkdownResult.emit(markdown_html)

    def getTime(self) -> str:
        now_time = time_time()
        now_time_format = now_time - self.start_time
        millisecond = int(round(float("{:.3f}".format(now_time_format)),3)%1*1000)
        format_time = time_strftime("%M:%S", time_gmtime(now_time_format))
        format_millisecond = "{:0>3d}".format(millisecond)
        return f"[{format_time}.{format_millisecond}]"

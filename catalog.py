import requests
from mock_useragent import UserAgent
from regular import Json
from lxml import etree
import re
from log import Logger

log = Logger().getlog()


class Catalog:
    def __init__(self, homeurl: str, whichRule: int):  # 需要传入搜索结果中的url,和第几个规则
        self.homeurl = homeurl
        self.whichRule = whichRule
        self.now_rule = self.getUserRule()  # 当前规则
        self.no_rule = "whitesev"
        self.catalog_rule = self.now_rule["catalog"]  # 当前规则的目录规则
        self.charset = self.now_rule["charset"]

        self.bookid = re.findall(r"\d+\d*", self.homeurl)
        self.model = self.catalog_rule["model"]
        self.headers = {
            "User-Agent": UserAgent().random_chrome,
            "Referer": self.homeurl
        }

        # 共有三个模式
        # 1是搜索结果的url中就含有全部的目录页
        # 2是搜索结果的url中目录不全，需要跳转到新页面获取全部目录
        # 3是搜索结果的url中目录不全，不全的部分需要ajax请求获取
        # 4是搜索结果的url中目录不全，需要跳转到新页面获取全部目录，但新目录页也不全，需要ajax请求获取剩余的

    def main(self) -> list:
        homeResp = self.getHome()
        if self.model == 1:
            log.info("模式1：")
            return self.getCatalog(self.homeurl)
        elif self.model == 2:
            log.info("模式2：")
            catalog_url = self.getToCatalogUrl_two_four(homeResp)
            if catalog_url == self.now_rule["bookSourceUrl"]:
                log.info("xpath解析到！！")
            else:
                return self.getCatalog(catalog_url)
        elif self.model == 3:
            log.info("模式3：")
        elif self.model == 4:
            log.info("模式4：")
            catalog_url = self.getToCatalogUrl_two_four(homeResp)
            if catalog_url == self.now_rule["bookSourceUrl"]:
                log.warning("xpath解析错误！！")
                return []
            else:
                return self.getCatalog(catalog_url)
        else:
            log.info("模式5：")
            chapterList = []
            while True:
                chapterList.extend(self.getCatalog(url=self.homeurl))
                log.info("当前章节%s" % str(chapterList))
                nowUrlResp = self.getResp(url=self.homeurl)
                if nowUrlResp is None: break
                nextPageUrl = self.getNextPageUrl(resp=nowUrlResp)
                if nextPageUrl is None: break
                self.homeurl = nextPageUrl if "http" in nextPageUrl else self.now_rule["bookSourceUrl"] + nextPageUrl
                log.info("下一页url%s" % self.homeurl)
            return chapterList

    def getNextPageUrl(self, resp: str) -> str:
        html = etree.HTML(resp)
        try:
            nextPageXpath = self.catalog_rule["nextPage"] or self.no_rule
            nextPage = html.xpath(nextPageXpath)[0] if html.xpath(nextPageXpath) else ""
            if nextPage:
                return nextPage
            else:
                return None
        except etree.XPathEvalError:
            self.sendHTML(s=f"<br>{self.getTime()} └语法错误")
            return None

    def getResp(self, url: str) -> str:
        headers = {
            "User-Agent": UserAgent().random_chrome
        }
        try:
            homeResp = requests.get(url=url, headers=headers, timeout=10, verify=False).content.decode(self.charset)
            return homeResp
        except requests.Timeout:
            log.warning("获取网站连接超时")
            return None

    def getHome(self) -> str:  # 获取目录页  按情况判断是否请求目录页或api
        log.info("当前需要请求的目录url:%s" % self.homeurl)
        log.info("book名：%s" % self.bookid)
        homeResp = requests.get(url=self.homeurl, headers=self.headers,verify=False).content.decode(self.charset)
        return homeResp

    def getToCatalogUrl_two_four(self, resp: str) -> str:  # 获取目录详情页的链接
        html = etree.HTML(resp)
        catalog_url_su = html.xpath(self.catalog_rule["toUrl"])[0] if html.xpath(self.catalog_rule["toUrl"]) else ""
        catalog_url = self.now_rule["bookSourceUrl"] + catalog_url_su
        log.info("目录详情页的url:%s" % catalog_url)
        return catalog_url

    def getCatalog(self, url: str) -> list:  # 获取目录页 所有目录
        try:
            catalog_resp = requests.get(url=url, headers=self.headers,verify=False).content.decode(self.charset)
            html = etree.HTML(catalog_resp)
            element = html.xpath(self.catalog_rule["element"])
            bookurl_rule = self.catalog_rule["bookUrl"]
            chapterName_rule = self.catalog_rule["chapterName"]
            catalog_list = []
            for i in element:
                catalog_dict = {
                    "bookUrl": "",
                    "chapterName": ""
                }
                bookurl = i.xpath(bookurl_rule)
                chapterName = i.xpath(chapterName_rule)
                bookurl_new = bookurl[0] if bookurl else ""
                if bookurl_new and bookurl_new[0:4] != "http":
                    bookurl_new = self.now_rule["bookSourceUrl"] + bookurl_new
                catalog_dict["bookUrl"] = bookurl_new
                catalog_dict["chapterName"] = chapterName[0] if chapterName else ""
                catalog_list.append(catalog_dict)
        except Exception as err:
            log.error(err)
        return catalog_list

    def getUserRule(self) -> list:
        return Json().getData()[self.whichRule]

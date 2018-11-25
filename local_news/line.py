#coding:UTF-8

#standard
from abc import ABCMeta, abstractmethod
import configparser as cp
from datetime import datetime
from datetime import timedelta
import os
import random
import requests
import sys
import time
import ssl

#package
from bs4 import BeautifulSoup
import schedule

#local
from url import loopRequest


class News(metaclass=ABCMeta):

    def __init__(self, url):
        self._url = url
        self._soup = None
        self.prepareSoupBase(self._url)

    def prepareSoupBase(self, url):
        html = loopRequest(url)
        self._soup = BeautifulSoup(html, "html.parser")

    @abstractmethod
    def track(self):
        pass

class SorachiLocalNews(News):

    def __init__(self):
        self._domain = "https://www.hokkaido-np.co.jp"
        self._branch = "/local/l_sorachi"
        _url = self._domain + self._branch
        super().__init__(_url)

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def branch(self):
        return self._branch

    @branch.setter
    def branch(self, value):
        self._branch = value

    def track(self):
        articles = self._soup.find("ul", class_="categoryArchiveList")
        links = articles.find_all("a")

        topics = []

        for item in links:
            article_date = item.find("div", class_="categoryArchiveItemDate").text.strip()
            if self.fromDate(article_date, 1):
                link = self._domain + item["href"]
                title = item.find("div", class_="categoryArchiveItemTitle").text.strip()
                topics.append([link,title])

        index = random.randrange(len(topics))
        
        return topics[index]

    def fromDate(self, from_date, day_span):
        
        dst = False
        now = datetime.now()
        target_datetime = datetime.strptime(str(now.year) + "/" +from_date, '%Y/%m/%d %H:%M')
        time_span = now - target_datetime

        if time_span.days <= day_span:
            dst = True
        return dst

class AsahikawaLocalNews(SorachiLocalNews):
    pass

class Composer:

    #global
    _url = "https://notify-api.line.me/api/notify"

    def __init__(self, ini_file, messages=[]):
        self._token = self.configParse(ini_file)
        self._messages = messages

    def configParse(self, ini):
        config = cp.ConfigParser()
        config.read(ini)
        return config["line-notify"]["token"]

    def execute(self):
        headers = {"Authorization" : "Bearer "+ self._token}
        payload = {"message" :  "\n" + "\n".join(self._messages)}

        r = requests.post(self._url ,headers = headers ,params=payload)


def job(file):
    s = SorachiLocalNews()

    #a = AsahikawaLocalNews()
    #a.branch = "/local/l_asahikawa"
    #a.prepareSoupBase(a.domain + a.branch)

    texts = ["[" + datetime.now().strftime("%Y/%m/%d %H:%M") + "]" + "サーバから配信"]
    texts += s.track()

    c = Composer(file, texts)
    c.execute()


if __name__ == '__main__':
    
    ssl._create_default_https_context = ssl._create_unverified_context
    args = sys.argv

    if len(args) == 2:
        root, ext = os.path.splitext(args[1])
        if ext != ".ini":
            print("[USAGE] you should use a ini_file.")
            sys.exit()
        if not os.path.isfile(args[1]):
            print("[USAGE] This file does not exist.")
            sys.exit()
    else :
        print("[USAGE] It is not a file parameter.")
        sys.exit()

    func = lambda : job(args[1])

    #平日のみ配信
    schedule.every().monday.at(alerm_time).do(func)
    schedule.every().tuesday.at(alerm_time).do(func)
    schedule.every().wednesday.at(alerm_time).do(func)
    schedule.every().thursday.at(alerm_time).do(func)
    schedule.every().friday.at(alerm_time).do(func)

    while True:
        schedule.run_pending()
        time.sleep(1)


import hashlib
import json
import random
import time
from threading import Thread

import requests


class Function:
    sessionId = "d41d8cd98f00b204e9800998ecf8427ebb894a754b11a99f32662e5a4959183da50bc127ce37e0ac63273f7cb52c67b7"
    url = "https://api.bmobcloud.com/1/functions/"
    baseUrlLen = url.find("/1/functions/")
    # proxies = {"http": "http://127.0.0.1:5555", "https": "http://127.0.0.1:5555"}
    proxies = {"http": None, "https": None}
    verify = True
    headers = {
        "Host": "api.bmobcloud.com",
        "Connection": "keep-alive",
        "X-Bmob-SDK-Type": "wechatApp",
        "X-Bmob-Safe-Sign": "",
        "content-type": "application/json",
        "X-Bmob-Safe-Timestamp": '0',
        "X-Bmob-Secret-Key": "c90f6a12abfd60bf",
        "X-Bmob-Noncestr-Key": "Akw1qpbbJ0JOeKaV",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123c) NetType/WIFI Language/zh_CN",
        "Referer": 'https://servicewechat.com/wx82259614dc2635bd/8/page-frame.html'
    }
    json = {}
    response = ""

    def preHeaders(self):
        Timestamp = int(time.time())
        self.headers["X-Bmob-Safe-Timestamp"] = str(Timestamp)

        # s = randomString()
        # value: 路径    pull：时间戳    data.securityCode："122468"    tipCount：随机串
        # str:/1/functions/FOX_Login1649406578122468dRDnBdjL0mAFlk71   ans:b9887513034c38788ab2b6c5c4537d37
        Safe_Sign = hexMd5(self.url[self.baseUrlLen::] + str(Timestamp) + "122468" + "Akw1qpbbJ0JOeKaV")
        self.headers["X-Bmob-Safe-Sign"] = Safe_Sign

    def request(self):
        self.preHeaders()
        response = requests.post(url=self.url, proxies=self.proxies, headers=self.headers,
                                 json=self.json, verify=self.verify).json()
        self.response = json.loads(response["result"])
        return self.response


class FunctionFoxCats(Function):
    def __init__(self):
        self.json = {
            "type": "team",
            "ks": 0,
            "key": "ALL",
            "apptype": "wxapp"
        }
        self.url += "FOX_cats"


class FunctionFoxSingersOfTeam(Function):
    def __init__(self, team_id):
        self.json = {
            "apptype": "wxapp",
            "sessionid": self.sessionId,
            "teamid": team_id,
            "ks": 0,
            "kind": "all"
        }
        self.url += "FOX_singers_of_team"


class FunctionFoxSingersConcertSongs(Function):
    def __init__(self, singer_id, type, singer, team):
        self.json = {
            "apptype": "wxapp",
            "sessionid": self.sessionId,
            "type": type,
            "team": team,
            "singer": singer,
            "singerid": singer_id,
            "ks": 0,
            "kind": "all"
        }
        self.url += "FOX_singers_concert_songs"


class FunctionFoxSongs(Function):
    def __init__(self, song_id):
        self.json = {
            "singer": "",
            "songtime": "",
            "songid": song_id,
            "sessionid": self.sessionId,
            "team": "",
            "apptype": "wxapp"
        }
        self.url += "FOX_songs"


class FunctionFoxRandom(Function):
    def __init__(self, conert_id, song_id):
        self.json = {
            "songid": song_id,
            "ordertype": "songslist",
            "conertid": conert_id,
            "apptype": "wxapp",
            "sessionid": self.sessionId,
            "val": "sameconcert",
            "key": "sameconcert",
            "ks": 0
        }

        self.url += "FOX_random"


class FunctionFOXSearchAll(Function):
    def __init__(self, str):
        self.json = {
            "apptype": "wxapp",
            "sessionid": self.sessionId,
            "ks": 0,
            "kind": "search",
            "type": "no",
            "str": str
        }

        self.url += "FOX_search_all"


def task():
    while True:
        for i in range(8, 13):
            c = ""
            for idx in range(i + 1):
                c += random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            # print(threading.currentThread().getName() + "线程 " + c)
            if b == hexMd5(a + c):
                print(c)


def hexMd5(str):
    # 创建md5对象
    hl = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))

    return hl.hexdigest()


if __name__ == '__main__':
    a = '/bf62ea3abd7f4d00a44157d82e50261d/0aa6909c174d41caa550b4100a839c21-c359af3f947c77e71e5a2bc0df947aeb-sd.mp4-1649694728-f389bc4419364251994fcc6d52f4aaeb-0-'
    b = '240296293a8687b529a71376c0c4c517'

    for i in range(10):
        t = Thread(target=task)
        t.start()

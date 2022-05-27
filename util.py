import hashlib
import json
import os
import time
from random import random
from urllib.request import urlopen

from aria2_rpc import Aria2RPC

from entity import VideoDetails
from functions import FunctionFoxSongs, FunctionFoxSingersOfTeam

__cnt__ = 10
__URL_MAX_LEN__ = 1
cmd = "aria2c --dir={} --out={} {}"
# cmd = "IDMan.exe  /p {} /f {} /d {}"

__remote__ = 0
__max__wait__size__ = 8000
__time__ = 0
basePath = "E:/阿里云盘/songss"
basePath1 = "E:/阿里云盘/songss"
# remoteBasePath = "/home/pi/disk/clouddrive/CloudDrive/阿里云盘/songs"
remoteBasePath = "/root/downloads"

# ip = '192.168.31.254'
# ip = '192.168.90.168'
ip = '149.28.81.55'
aria2rpc = Aria2RPC(ip, 6800, "8e2c30dd8f7bffc4751d")
__urls__ = []


def hexMd5(str):
    # 创建md5对象
    hl = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))

    return hl.hexdigest()


def randomString():
    chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
             "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    randomstring = ""
    for i in range(16):
        randomstring = randomstring + chars[int(61 * random())]
    return randomstring


def makePic(basePath, filename, url):
    path = basePath + '/' + filename
    path = path.replace('*', '')
    filename = filename.replace('*', '')
    filePath = path + '/##' + filename + ".jpg"
    if not os.path.exists(path):
        os.mkdir(path)
        print("文件夹：", path, " 创建成功")

    if not os.path.exists(filePath):
        time.sleep(0.5)
        url = url.strip()
        if os.system(cmd.format('"' + path + '"', '"##' + filename + '.jpg"', url)) == 0:
            print("文件：", filePath, " 创建成功")
        else:
            print(cmd.format(path, "##" + filename + ".jpg", url), " Error")
            return -1
    return 0


def wait_for_download():
    wait = True
    while __remote__:
        numWaiting = int(aria2rpc.getGlobalStat()["numWaiting"])
        if numWaiting > __max__wait__size__:
            if wait:
                print("wait.", end="")
                wait = False
            else:
                print(".", end="")
            secs = max((numWaiting - __max__wait__size__) / 4, 3)
            time.sleep(secs)
        else:
            if not wait:
                print("\n", end="")
            break


def makeVideo(basePath, detail, title, session):
    path = basePath
    v = detail.v["url"]
    res = upload(detail, path, title, v, "v")
    if res == 0:
        v = detail.i["urlgif"] if len(detail.i["urlgif"]) > 5 else detail.i["url"]
        res = download(path, title, v, "i")
        if res == -1:
            return -1
        elif res == 1:
            return 1
    elif res == 1:
        v = detail.i["urlgif"] if len(detail.i["urlgif"]) > 5 else detail.i["url"]
        if download(path, title, v, 'i') == -1:
            return -1
        else:
            return 1
    else:
        return -1

    detail.ok = 1
    session.commit()
    return 0


def upload(detail:VideoDetails, path, title, v, type):
    if len(v) > 5:
        if v.find("http://foxvod.zero248.top") != -1:
            wait_for_download()
            global __time__
            __time__ = int(time.time())
            FunctionFoxSongsResponse = FunctionFoxSongs(detail.id).request()
            if FunctionFoxSongsResponse["msg"] == 200:
                items = FunctionFoxSongsResponse["item"]
                for item in items:
                    if item["cid"] is not None and item["cid"] != "":
                        if type == 'v':
                            detail.v["url"] = v = item["v"]["url"]
                            detail.i = item['i']
                            # if v.rfind(".mp4") != -1:
                            #     v = v[:v.rfind(".mp4")]
                        # else:
                        #     detail.v = item["v"]
                        #     v = item["i"]["urlgif"] if len(item["i"]["urlgif"]) > 5 else item["i"]["url"]
                        #     # if v.rfind(".jpg") != -1:
                        #     #     v = v[:v.rfind(".mp4")]
                        type = 'i'
            elif FunctionFoxSongsResponse["msg"] == 400:
                global __cnt__
                __cnt__ += 1
                t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(t, "请求失败： ", FunctionFoxSongsResponse)
                with open("failDownload.txt", "a+", encoding='utf-8') as file:
                    file.writelines(t + " {}\n".format(detail))
                if __cnt__ == 30:
                    return -1
                else:
                    time.sleep(2)
                    return 1
            else:
                print(FunctionFoxSongsResponse)
                return -1
        # else:
        #
        #     # print("not startswith ", "http://foxvod.zero248.top")
        #     return 1
    if len(v) > 5:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), title)
        return download(path, title, v, type)

    return 1


def download(path, title: str, v, type):
    start = v.rfind("/")
    end = len(v) if v.rfind("?") == -1 else v.rfind("?")
    path = path.replace('*', '')
    title = title.replace('*', '')
    v = v.strip()
    if type == 'i':
        if not file_exists(path, path + '/' + title + "_" + v[start + 1:end]):
            if remote_download('"' + path + '"', '"' + title + "_" + v[start + 1:end] + '"', v) == 0:
                print("文件：", path + '/' + title + "_" + v[start + 1:end], " 创建成功")
                return 1
            # else:
            #     print(cmd.format(path, title + "_" + v[start + 1:end], v), " Error")
            #     return -1
    else:
        if not file_exists(path, path + '/' + title + "_" + v[start + 1:end] + '.mp4'):
            if remote_download('"' + path + '"', '"' + title + "_" + v[start + 1:end] + '.mp4' + '"', v) == 0:
                print("文件：", path + '/' + title + "_" + v[start + 1:end] + '.mp4', " 创建成功")
                return 1
            # else:
            #     print(cmd.format(path, title + "_" + v[start + 1:end] + '.mp4', v), " Error")
            #     return -1
    return 0


def file_exists(path, filename):
    if os.path.exists(filename):
        return True
    os.listdir(path)
    return os.path.exists(filename)


def getRealImg(item_id, singer):
    if singer.img.startswith("http://foxvod.zero248.top"):
        FoxSingersOfTeamResponse = FunctionFoxSingersOfTeam(item_id).request()
        if FoxSingersOfTeamResponse["msg"] == 200:
            items = FoxSingersOfTeamResponse["item"]
            for item in items:
                if item["singerid"] is not None and item["singerid"] == singer.singerid:
                    return item["img"]
    else:
        return singer.img


def remote_download(path: str, filename, url):
    if __remote__:
        path = path.replace(basePath, '')
        path = path.replace('"', '')[1:]
        filename = path + '/' + filename.replace('"', '')
        options = {"out": filename}

        # options["dir"] = path
        __urls__.append({"uri": [url], "options": options})
        if len(__urls__) == __URL_MAX_LEN__:
            idx = 0
            for i in __urls__:
                idx += 1
                print(idx, ": ", i)
            res = aria2rpc.addUris(__urls__)
            print(res)
            __urls__.clear()
    else:
        path = path.replace(basePath, basePath1)
        if os.system(cmd.format(path, filename, url)) != 0:
            time.sleep(90)
            return -1
        global __time__
        tmp = max(0, 120 - (int(time.time()) - __time__))
        # time.sleep(tmp + 5)
    return 0


# def download():
#     downData = [{
#         "jsonrpc": "2.0",
#         "method": "aria2.addUri",
#         "id": 1,
#         "params": [
#             'token:8e2c30dd8f7bffc4751d',
#             ["http://vshuping.file.alimmdn.com/videos/2155a697d6613a55"], {
#             }
#         ]
#     }, {
#         "jsonrpc": "2.0",
#         "method": "aria2.addUri",
#         "id": 1,
#         "params": [
#             'token:8e2c30dd8f7bffc4751d',
#             ["http://vshuping.file.alimmdn.com/videos/2155a697d6613a55"], {
#             }
#         ]
#     }, {
#         "jsonrpc": "2.0",
#         "method": "aria2.addUri",
#         "id": 1,
#         "params": [
#             'token:8e2c30dd8f7bffc4751d',
#             ["http://vshuping.file.alimmdn.com/videos/2155a697d6613a55"], {
#             }
#         ]
#     }]
#
#     jsonreq = json.dumps(downData).encode()
#     c = urlopen('http://192.168.31.254:6800/jsonrpc', jsonreq)
#     print(c.read())


if __name__ == '__main__':

    # print(aria2rpc.getGlobalStat())

    # # 单个下载
    # options = {
    #     "out": "test/sss.mp4",
    #     # 'dir': "/home/pi/disk/clouddrive/CloudDrive/阿里云盘",
    #     # 'dir': "",
    # }
    # resp = aria2rpc.addUri(['http://vshuping.file.alimmdn.com/videos/19229c36c69bac8b'], options=options)
    # print(resp)

    # # 多个下载
    # uris = []
    # uri = {"uri": ["http://vshuping.file.alimmdn.com/videos/3bf063f667c5a4c2"]}
    #
    # uris.append(uri)
    # uri["uri"] = ["http://vshuping.file.alimmdn.com/videos/2155a697d6613a55"]
    #
    # uris.append(uri)
    # uri["uri"] = ["http://vshuping.file.alimmdn.com/videos/d77ed4b5586b079b"]
    #
    # uris.append(uri)
    #
    # a = aria2rpc.addUris(uris)
    # print(a)

    #
    # v = 'abc'
    # print(v[:len(v) if v.rfind("b") == -1 else v.rfind("b")])
    pass

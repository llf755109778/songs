import hashlib
import os
import time
from random import random

from download import cmd
from functions import FunctionFoxSongs, FunctionFoxSingersOfTeam

__cnt__ = 0


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
        if os.system(cmd.format('"' + path + '"', '"##' + filename + '.jpg"', url)) == 0:
            print("文件：", filePath, " 创建成功")
        else:
            print(cmd.format(path, "##" + filename + ".jpg", url), " Error")
            return -1
    return 0


def makeVideo(basePath, detail, title, session):
    path = basePath + "/"
    v = detail.v["url"]
    res = upload(detail, path, title, v, "v")
    if res == 0:
        v = detail.i["urlgif"] if len(detail.i["urlgif"]) > 5 else detail.i["url"]
        res = upload(detail, path, title, v, "i")
        if res == -1:
            return -1
        elif res == 1:
            return 1
    elif res == 1:
        v = detail.i["urlgif"] if len(detail.i["urlgif"]) > 5 else detail.i["url"]
        if upload(detail, path, title, v, 'i') == -1:
            return -1
        else:
            return 1
    else:
        return -1

    detail.ok = 1
    session.commit()
    return 0


def upload(detail, path, title, v, type):
    if len(v) > 5:
        if v.startswith("http://foxvod.zero248.top"):
            time.sleep(1)
            FunctionFoxSongsResponse = FunctionFoxSongs(detail.id).request()
            if FunctionFoxSongsResponse["msg"] == 200:
                items = FunctionFoxSongsResponse["item"]
                for item in items:
                    if item["cid"] is not None and item["cid"] != "":
                        if type == 'v':
                            detail.v["url"] = v = item["v"]["url"]
                            # if v.rfind(".mp4") != -1:
                            #     v = v[:v.rfind(".mp4")]
                        else:
                            detail.v = item["v"]
                            v = item["i"]["urlgif"] if len(item["i"]["urlgif"]) > 5 else item["i"]["url"]
                            # if v.rfind(".jpg") != -1:
                            #     v = v[:v.rfind(".mp4")]
            else:
                global __cnt__
                __cnt__ += 1
                t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(t, "请求失败： ", FunctionFoxSongsResponse)
                with open("failDownload.txt", "a+", encoding='utf-8') as file:
                    file.writelines("t {}\n".format(detail))
                if __cnt__ == 10:
                    return -1
                else:
                    time.sleep(2)
                    return 1
        else:
            # print("not startswith ", "http://foxvod.zero248.top")
            return 1
    if len(v) > 5:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), title)
        if download(path, title, v, type) != 0:
            return -1
        else:
            return 0
    return 1


def download(path, title, v, type):
    start = v.rfind("/")
    end = v.rfind("?")
    # if type == 'v':
    path = path.replace('*', '')
    title = title.replace('*', '')
    if not os.path.exists(path + title + "_" + v[start + 1:end]):
        if os.system(cmd.format('"' + path + '"', '"' + title + "_" + v[start + 1:end] + '"', v)) == 0:
            print("文件：", path + title + "_" + v[start + 1:end], " 创建成功")
        else:
            print(cmd.format(path, title + "_" + v[start + 1:end], v), " Error")
            return -1
    # else:
        # if not os.path.exists(path + title + "_" + v[start + 1:end]):
        #     if os.system(cmd.format('"' + path + '"', '"' + title + "_" + v[start + 1:end] + '"', v)) == 0:
        #         print("文件：", path + title + "_" + v[start + 1:end], " 创建成功")
        #     else:
        #         print(cmd.format(path, title + "_" + v[start + 1:end], v), " Error")
        #         return -1
    return 0


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


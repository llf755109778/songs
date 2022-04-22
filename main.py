import os
import sys
from threading import Thread

from db import *
from functions import *

song_id = ""
__TIME__ = 0.5
iii = 0


def getFunctionFoxSongs(song_id, session):
    time.sleep(__TIME__)
    FunctionFoxSongsResponse = FunctionFoxSongs(song_id).request()
    if FunctionFoxSongsResponse["msg"] == 200:
        items = FunctionFoxSongsResponse["item"]
        for item in items:
            if item["cid"] is not None and item["cid"] != "":
                #  写入数据库
                session.execute(VideoDetails.__table__.insert(), item)
                print("song_id:{}, FunctionFoxSongsResponse:{}".format(song_id, items))
    elif FunctionFoxSongsResponse["msg"] == 400:
        # print("here is :", __file__, sys._getframe().f_lineno, "response code not 200!!!")
        with open("getFunctionFoxSongs.txt", "a+", encoding='utf-8') as file:
            file.writelines("song_id:{}\n".format(song_id))
        print("error: ", FunctionFoxSongsResponse)
        # global iii
        # if iii == 30:
        #     return -1
        # iii += 1
    else:
        with open("getFunctionFoxSongs.txt", "a+", encoding='utf-8') as file:
            file.writelines("song_id:{}\n".format(song_id))
        print("error: ", FunctionFoxSongsResponse)
        return -1
    return 0


def getFunctionFoxRandom(conert_id, session):
    time.sleep(__TIME__)
    FoxRandomResponse = FunctionFoxRandom(conert_id, song_id).request()
    if FoxRandomResponse["msg"] == 200:
        items = FoxRandomResponse["item"]
        for item in items:
            if item["id"] is not None and item["id"] != "":
                if getFunctionFoxSongs(item["id"], session) == -1:
                    return -1
                # 写入数据库
                session.execute(Video.__table__.insert(), item)
    else:
        # print("conert_id:{}, FoxRandomResponse:{}".format(conert_id, FoxRandomResponse))
        # print("here is :", __file__, sys._getframe().f_lineno, "response code not 200!!!")
        with open("getFunctionFoxRandom.txt", "a+", encoding='utf-8') as file:
            file.writelines("conert_id:{}, song_id:{}\n".format(conert_id, song_id))
    return 0


def getFunctionFoxSingersConcertSongs(singer_id, singer, team, session):
    types = ["songs"]
    for type in types:
        time.sleep(__TIME__)
        FoxSingersConcertSongsResponse = FunctionFoxSingersConcertSongs(singer_id, type, singer, team).request()
        if FoxSingersConcertSongsResponse["msg"] == 200:
            items = FoxSingersConcertSongsResponse["item"]
            for item in items:
                if item["type"] is not None and item["type"] != "":
                    if type == "songs":
                        global song_id
                        song_id = items[0]["id"]
                        if getFunctionFoxSongs(item["id"], session) == -1:
                            return -1
                        # 写入数据库
                        session.execute(Video.__table__.insert(), item)
                    else:
                        if getFunctionFoxRandom(item["time"], session) == -1:
                            return -1
                        # 写入数据库
                        session.execute(Concert.__table__.insert(), item)

        else:

            print("singer_id:{}, singer:{}, type:{}, team:{}, response:{}".format(singer_id, singer, type, team,
                                                                                  FoxSingersConcertSongsResponse))
            with open("getFunctionFoxSingersConcertSongs.txt", "a+", encoding='utf-8') as file:
                file.writelines("singer_id:{}, singer:{}, team:{}\n".format(singer_id, singer, team, ))
            # print("here is :", __file__, sys._getframe().f_lineno, "response code not 200!!!")

    return 0


def getFoxSingersOfTeam(item_id, session):
    time.sleep(__TIME__)
    FoxSingersOfTeamResponse = FunctionFoxSingersOfTeam(item_id).request()
    if FoxSingersOfTeamResponse["msg"] == 200:
        items = FoxSingersOfTeamResponse["item"]
        for item in items:
            if item["singerid"] is not None and item["singerid"] != "":
                if session.query(Singer).filter_by(singerid=item["singerid"]).count() <= 0:
                    print("item_id:{}, singerid:{}, item:{}".format(item_id, item["singerid"], item))
                    if getFunctionFoxSingersConcertSongs(item["singerid"], item["singer"], item["team"], session) == -1:
                        return -1
                    # 写入数据库
                    session.execute(Singer.__table__.insert(), item)
                    session.commit()
    else:
        # print("item_id:{}, FoxSingersOfTeamResponse:{}".format(item_id, FoxSingersOfTeamResponse))
        # print("here is :", __file__, sys._getframe().f_lineno, "response code not 200!!!")
        with open("getFoxSingersOfTeam.txt", "a+", encoding='utf-8') as file:
            file.writelines("item_id:{}\n".format(item_id))

    return 0


def task(items, i):
    # 去连接池中获取一个连接
    session = DBSession()
    failed = ["g"]
    with open("foo{}.txt".format(i), "a+", encoding='utf-8') as foo:
        for idx in range(270):
            item = items[1 * i + idx]
            # item = items[10]
            if item["id"] is not None and item["id"] != "":
                if session.query(Team).filter_by(team=item["team"], id=item["id"]).count() <= 0:
                    if getFoxSingersOfTeam(item["id"], session) == -1:
                        # print("here is :", sys._getframe().f_lineno, "response code not 200!!!")
                        # global iii
                        # if iii == 30:
                        #     return -1
                        failed.append(item["id"])
                        session.rollback()
                    else:
                        # print("item_id:{}".format(item["id"]))
                        # 写入数据库
                        session.execute(Team.__table__.insert(), item)
                        session.commit()
        foo.write(str(failed) + "\n")
    # 将连接交还给连接池
    session.close()


if __name__ == '__main__':
    # 建数据表 配置在entity.py 中
    Base.metadata.create_all()

    # os.system('chcp 65001')
    # hh = "aria2c --dir=E:/阿里云盘 --out=123 " + "\rhttp://shuping.image.alimmdn.com/foxsongs/20856000.jpg@360w.jpg"
    # print(os.system("aria2c --dir=E:/阿里云盘 --out=123 http://vshuping.file.alimmdn.com/videos/63ddd9480fbc29e7"))
    # print(os.system(hh))

    # 获取所以组合
    FoxCatsResponse = FunctionFoxCats().request()
    if FoxCatsResponse["msg"] == 200:
        items = FoxCatsResponse["item"]
        for i in range(1):
            t = Thread(target=task, args=(items, i))
            t.start()

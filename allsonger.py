import json
__MAX__ = 47248
__MIN__ = 0

from os import listdir

from sqlalchemy import or_

from functions import FunctionFOXSearchAll
from main import getFunctionFoxSongs
from download import *
from util import basePath


def getDownload(play_no, session):
    FunctionFOXSearchAllResponse = FunctionFOXSearchAll(play_no).request()
    if FunctionFOXSearchAllResponse["msg"] == 200:
        items = FunctionFOXSearchAllResponse["item"]
        for item in items:
            if item["id"] is not None and item["id"] != "":
                if getFunctionFoxSongs(item["id"], session) == -1:
                    print("error: ", item)
                    return -1
                if session.query(Video).filter_by(id=item["id"]).count() == 0:
                    session.execute(Video.__table__.insert(), item)
                # 写入数据库
                return item["id"]
    elif FunctionFOXSearchAllResponse["msg"] == 100:
        return 0
    else:
        return -1


def update():
    session = DBSession()
    for i in range(__MIN__, __MAX__ + 1):
        # if session.query(Download).filter_by(playno="#" + str(i)).count() == 0:
            lists = session.query(VideoDetails).filter_by(playno="#" + str(i))
            tmp = {}
            if lists.count() == 0:
                session.commit()
                res = getDownload(i, session)
                if res == -1:
                    print(i, res)
                    return -1
                tmp["ok"] = 0
                tmp["isvideo"] = res if res == 0 else 1
                tmp["id"] = res
                tmp["playno"] = "#" + str(i)
            else:
                tmp["ok"] = lists[0].ok
                tmp["isvideo"] = 1 if len(lists[0].v["url"]) > 5 else 0
                tmp["id"] = lists[0].id
                tmp["playno"] = lists[0].playno
            session.execute(Download.__table__.insert(), tmp)
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(t, " download:", tmp)
    session.commit()
    session.close()
    return 0


def repair_get_error():
    session = DBSession()
    queryAns = session.query(Download) \
        .filter(Download.id == '0')
    for tmp in queryAns:
        i = tmp.playno[1:]
        lists = session.query(VideoDetails).filter_by(playno="#" + i)
        if lists.count() == 0:
            res = getDownload(i, session)
            if res == -1:
                print(i, res)
                return -1
            tmp.isvideo = res if res == 0 else 1
            tmp.id = res
        else:
            tmp.isvideo = 1 if len(lists[0].v["url"]) > 5 else 0
            tmp.id = lists[0].id
        session.commit()
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(t, " download:", tmp)
    session.commit()
    session.close()
    return 0


def download():
    session = DBSession()
    lists = session.query(Download)\
        .filter(or_(Download.ok == 0, Download.ok.is_(None)))\
        .filter(Download.isvideo == 1)\
        .filter(Download.id != '0')\
        .filter(Download.idd >= 47228)
    i = 1
    # lists = session.query(Download).filter(or_(Download.ok == 0, Download.ok.is_(None)))\
    #     .filter(Download.id != '0').filter(Download.idd > 41624)
    if lists.count() != 0:
        for list in lists:
            print(i)
            i += 1
            res = video(list, session)
            if res == -1:
                session.close()
                return -1
            elif res == 1:
                pass
            else:
                list.ok = 1
                session.commit()
    session.close()


def video(info, session):
    lists = session.query(Video).filter_by(id=info.id)
    for i in lists:
        details = session.query(VideoDetails).filter_by(id=i.id)
        for detail in details:
            path = basePath + '/' + detail.stillbtns["team"] + '/' + detail.stillbtns["singer"]
            path = path.replace('*', '')
            if not os.path.exists(path):
                os.makedirs(path)
                print("文件夹：", path, " 创建成功")
            result = makeVideo(path, detail, detail.title2 + "_" + i.title, session)
            if result == 0:
                print(detail)
                i.ok = 1
                session.commit()
            elif result == -1:
                return -1
            else:
                return 1
    return 0


def readSong_ids():
    song_ids = []
    with open("getFunctionFoxSongs.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line[0:8] == 'song_id:':
                song_ids.append(line[8:-1])
    return song_ids


def writeSong_ids(fail_ids):
    with open("getFunctionFoxSongs.txt", "w", encoding='utf-8') as file:
        for song_id in fail_ids:
            file.writelines("song_id:{}\n".format(song_id))


def insert_video(play_no, session):
    time.sleep(0.3)
    FunctionFOXSearchAllResponse = FunctionFOXSearchAll(play_no).request()
    if FunctionFOXSearchAllResponse["msg"] == 200:
        items = FunctionFOXSearchAllResponse["item"]
        for item in items:
            if item["id"] is not None and item["id"] != "":
                session.execute(Video.__table__.insert(), item)
    elif FunctionFOXSearchAllResponse["msg"] == 400:
        return 0
    else:
        return -1
    return 1


def insert_by_song_id():
    session = DBSession()
    song_ids = readSong_ids()
    fail_ids = []
    flag = 0
    for song_id in song_ids:
        if session.query(VideoDetails).filter_by(id=song_id).count() == 0:
            if flag == 0:
                time.sleep(0.7)
                FunctionFoxSongsResponse = FunctionFoxSongs(song_id).request()
                if FunctionFoxSongsResponse["msg"] == 200:
                    items = FunctionFoxSongsResponse["item"]
                    for item in items:
                        if item["cid"] is not None and item["cid"] != "":
                            res = 1
                            if session.query(Video).filter_by(id=song_id).count() == 0:
                                res = insert_video(item["playno"][1:], session)
                            if res == -1:
                                fail_ids.append(song_id)
                                flag = 1
                                session.rollback()
                            elif res == 0:
                                fail_ids.append(song_id)
                                session.rollback()
                                continue
                            else:
                                #  写入数据库
                                session.execute(VideoDetails.__table__.insert(), item)
                                session.commit()
                                print("song_id:{}, FunctionFoxSongsResponse:{}".format(song_id, items))
                elif FunctionFoxSongsResponse["msg"] == 400:
                    fail_ids.append(song_id)
                    print("error: ", FunctionFoxSongsResponse)
                else:
                    fail_ids.append(song_id)
                    print("error: ", FunctionFoxSongsResponse)
                    flag = 1
            else:
                fail_ids.append(song_id)
    writeSong_ids(fail_ids)
    session.close()


def readDownload_error():
    paths = []
    with open("download_error.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            list = line.strip().split("|")
            if len(list) >= 3:
                # print(list)
                path = ""
                for i in range(2, len(list)):
                    path += list[i] + '/'
                paths.append(path + list[0])
    return paths


def writeDownload_error(fail_paths):
    lines = []
    with open("download_error.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
    with open("download_error.txt", "w", encoding='utf-8') as file:
        for fail_path in fail_paths:
            if fail_path < len(lines):
                line = lines[fail_path].strip()
                file.writelines(line + '\n')


def repair_download_error():
    session = DBSession()
    Download_errors = readDownload_error()
    fail_download_errors = []
    flag = 0
    for Download_error in Download_errors:
        if os.path.exists(basePath + '/' + Download_error):
            os.remove(basePath + '/' + Download_error)
            print("delete ", basePath + '/' + Download_error)
            # TODO 操作数据库
        else:
            fail_download_errors.append(flag)
        flag += 1
    writeDownload_error(fail_download_errors)
    session.close()


def remove_tmp():
    for file_name in listdir(basePath):
        if file_name.endswith('.mp4.tmp'):
            os.remove(basePath + file_name)
        elif file_name.endswith('.jpg.tmp'):
            os.remove(basePath + file_name)
        elif file_name.endswith('.jpg.aria2'):
            os.remove(basePath + file_name)
        elif file_name.endswith('.mp4.aria2'):
            os.remove(basePath + file_name)


if __name__ == '__main__':
    Base.metadata.create_all()
    # if update() == -1:
    #     print("download 失败")
    # repair_get_error()
    # # 待测试
    # repair_download_error()
    # insert_by_song_id()
    # remove_tmp()
    if download() == -1:
        print("download 失败")

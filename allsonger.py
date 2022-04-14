import json
__MAX__ = 47248
__MIN__ = 0


from functions import FunctionFOXSearchAll
from main import getFunctionFoxSongs
from download import *


def getDownload(play_no, session):
    FunctionFOXSearchAllResponse = FunctionFOXSearchAll(play_no).request()
    if FunctionFOXSearchAllResponse["msg"] == 200:
        items = FunctionFOXSearchAllResponse["item"]
        for item in items:
            if item["id"] is not None and item["id"] != "":
                if getFunctionFoxSongs(item["id"], session) == -1:
                    return -1
                if session.query(Video).filter_by(id=item["id"]).count() == 0:
                    session.execute(Video.__table__.insert(), item)
                # 写入数据库
                return item["id"]
    else:
        return -1


def update():
    session = DBSession()
    for i in range(__MIN__, __MAX__ + 1):
        if session.query(Download).filter_by(playno="#" + str(i)).count() == 0:
            lists = session.query(VideoDetails).filter_by(playno="#" + str(i))
            tmp = Download()
            if lists.count() == 0:
                res = getDownload(i, session)
                if res != -1:
                    print(i)
                    return -1
                tmp.ok = 0
                tmp.isvideo = 1
                tmp.id = res
                tmp.playno = "#" + str(i)
            else:
                tmp.ok = lists[0].ok
                tmp.isvideo = 1 if len(lists[0].v["url"]) > 5 else 0
                tmp.id = lists[0].id
                tmp.playno = lists[0].playno
            session.execute(Download.__table__.insert(), tmp)
            session.commit()
    session.close()
    return 0


def download():
    session = DBSession()
    lists = session.query(Download).filter_by(ok=0)
    if lists.count() != 0:
        for list in lists:
            if video(list, session) == -1:
                session.close()
                return -1
    session.close()


def video(info, session):
    lists = session.query(Video).filter_by(id=info.id)
    for i in lists:
        details = session.query(VideoDetails).filter_by(id=i.id)
        for detail in details:
            path = basePath + '/' + details.stillbtns["team"] + '/' + details.stillbtns["Second"]
            if not os.path.exists(path):
                os.mkdir(path)
                print("文件夹：", path, " 创建成功")
            result = makeVideo(path, detail, i.title, session)
            if result == 0:
                i.ok = 1
                session.commit()
            else:
                return -1


if __name__ == '__main__':
    if update() == -1:
        print("download 失败")
    if download() == -1:
        print("download 失败")

﻿import os

from db import DBSession
from entity import *
from util import *


def video(singer, basePath, session):
    res = 0
    lists = session.query(Video).filter_by(team=singer.team, singer=singer.singer, singerid=singer.singerid)
    for i in lists:
        if i.ok != 1:
            vedio_details = session.query(VideoDetails).filter_by(id=i.id)
            for detail in vedio_details:
                if detail.ok != 1:
                    result = makeVideo(basePath, detail, i.title, session)
                    if result == 0:
                        i.ok = 1
                        session.commit()
                    elif result == -1:
                        return -1
                    else:
                        res = 1
        # break
    return res


def singer(team, team_name, basePath, session):
    res = 0
    lists = session.query(Singer).filter_by(team=team_name)
    for i in lists:
        if i.ok != 1:
            img = getRealImg(team.id, i)
            if makePic(basePath, i.singer, img) == 0:
                print("download singer:{}", i)
                result = video(i, basePath + '/' + i.singer, session)
                if result == 0:
                    i.ok = 1
                    session.commit()
                elif result == 1:
                    res = 1
                else:
                    return -1
            else:
                return -1
    return res


def team():
    res = 0
    session = DBSession()
    lists = session.query(Team).all()
    p = 0
    h = 30
    for i in lists:
        if p < h:
            p += 1
            continue
        if i.ok != 1:
            if makePic(basePath, i.team, i.img) == 0:
                print("download team :{}", i)
                res = singer(i, i.team, basePath + '/' + i.team, session)
                if res == 0:
                    i.ok = 1
                    session.commit()
                elif res == -1:
                    return -1
                else:
                    res = 1
            else:
                return -1
    return res


if __name__ == '__main__':
    if team() == 0:
        print("任务完成")
    else:
        print("任务失败")
    '''
    IDMan.exe /f 123.mp4 /p E:\阿里云盘 /d "http://yizhen.file.alimmdn.com/videos/24da78aaf7fa4152"
    
    
    '''
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

__LEN__ = 255
engine = create_engine('mysql://root:123cnm@localhost/test?charset=utf8',
                       max_overflow=10,  # 超过连接池大小外最多创建的连接
                       pool_size=30,  # 连接池大小
                       pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       # echo=True
                       )
Base = declarative_base(engine)


class Team(Base):
    __tablename__ = 'Team'
    idd = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    id = Column(String(__LEN__))
    team = Column(String(__LEN__), comment="团名")
    key = Column(String(__LEN__), comment="查询关键字")
    singer = Column(String(__LEN__))
    time = Column(String(__LEN__))
    title = Column(String(__LEN__))
    img = Column(String(__LEN__), comment="图片链接")
    open = Column(Integer(), nullable=False)
    ok = Column(Integer())

    def __str__(self):
        return 'Team: idd:{}, id:{}, team:{}, key:{}, singer:{}, ' \
               'time:{}, title:{}, img:{}, open:{}, ok:{}'.format(self.idd, self.id, self.team, self.key, self.singer,
                                                                  self.time, self.title, self.img, self.open, self.ok)


class Singer(Base):
    __tablename__ = 'Singer'
    id = Column(String(__LEN__), primary_key=True)
    type = Column(String(__LEN__))
    team = Column(String(__LEN__), comment="团名")
    singerid = Column(String(__LEN__))
    singer = Column(String(__LEN__))
    time = Column(String(__LEN__))
    title = Column(String(__LEN__))
    img = Column(String(__LEN__))
    ok = Column(Integer())

    def __str__(self):
        return 'Singer: id:{}, type:{}, team:{}, singerid:{}, singer:{}, ' \
               'time:{}, title:{}, img:{}, ok:{}'.format(self.id, self.type, self.type, self.singerid, self.singer,
                                                         self.time, self.title, self.img, self.ok)


class Video(Base):
    __tablename__ = 'Video'
    idd = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    id = Column(String(__LEN__), primary_key=True)
    isVideo = Column(Integer())
    type = Column(String(__LEN__))
    team = Column(String(__LEN__))
    singerid = Column(String(__LEN__))
    singer = Column(String(__LEN__))
    time = Column(String(__LEN__))
    title = Column(String(__LEN__))
    img = Column(String(__LEN__))
    hidetitle = Column(Integer())
    ok = Column(Integer())

    def __repr__(self):
        return 'Video: idd:{}, id:{}, isVideo:{}, type:{}, team:{}, singerid:{}, singer:{}, time:{}, title:{}, ' \
               'img:{}, hidetitle:{}, ok:{}'.format(self.idd, self.id, self.isVideo, self.type, self.team,
                                                    self.singerid, self.singer, self.time, self.title, self.img,
                                                    self.hidetitle, self.ok)


class VideoDetails(Base):
    __tablename__ = 'Video_details'
    idd = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(__LEN__))
    playno = Column(String(__LEN__))
    stillbtns = Column(JSON())
    title2 = Column(String(__LEN__))
    cid = Column(String(__LEN__))
    id = Column(String(__LEN__))
    i = Column(JSON())
    v = Column(JSON(), comment="视频链接")
    ok = Column(Integer())

    def __repr__(self):
        return 'VideoDetails: idd:{}, name:{}, playno:{}, stillbtns:{}, title2:{}, cid:{}, id:{}, i:{}, v:{},' \
               ' ok:{}'.format(self.idd, self.name, self.playno, self.stillbtns, self.title2,
                               self.cid, self.id, self.i, self.v, self.ok)


class Concert(Base):
    __tablename__ = 'concert'
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    type = Column(String(__LEN__))
    team = Column(String(__LEN__))
    singer = Column(String(__LEN__))
    singerid = Column(String(__LEN__))
    time = Column(Integer())
    title = Column(String(__LEN__))
    img = Column(String(__LEN__))
    hidetitle = Column(Integer())
    ok = Column(Integer())

    def __repr__(self):
        return 'Concert: id:{}, type:{}, team:{},  singer:{}, singerid:{}, time:{}, title:{}, ' \
               'img:{}, hidetitle:{}, ok:{}'.format(self.id, self.type, self.team,
                                                    self.singer, self.singerid, self.time, self.title, self.img,
                                                    self.hidetitle, self.ok)


class Download(Base):
    __tablename__ = 'download'
    idd = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    id = Column(String(255))
    playno = Column(String(255))
    isvideo = Column(Integer())
    ok = Column(Integer())

    def __repr__(self):
        return 'Download: idd:{}, id:{}, playno:{}, isvideo:{}, ok:{}'.format(self.idd, self.id, self.playno,
                                                                              self.isvideo,  self.ok)

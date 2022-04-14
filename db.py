import datetime

from sqlalchemy.orm import sessionmaker, scoped_session

from entity import *

DBSession = sessionmaker(bind=engine)
# Session = scoped_session(DBSession)


if __name__ == '__main__':
    # 使用声明基类的 metadata 对象的 create_all 方法创建数据表：
    Base.metadata.create_all()
    session = DBSession()
    # a = {"id": "888885", "team": "10X10", "key": "a", "singer": "", "time": "", "title": "10X10",
    #      "img": "https://bytxpic.image.alimmdn.com/fox/10x10.jpg@720.jpg", "open": 1}
    # employee = Team(**a)
    # session.execute(Team.__table__.insert(), a)
    # session.add(employee)
    a = session.query(Team).filter_by(id="026").count()
    session.commit()

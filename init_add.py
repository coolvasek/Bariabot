from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class Shop(Base):
    __tablename__ = 'shops2'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tel = Column(Integer)
    address = Column(String)
    type = Column(String)
    square = Column(Integer)
    square_sell = Column(Integer)
    floor = Column(Integer)
    count_room = Column(Integer)
    rent = Column(Integer)
    comment = Column(String)

    chat_id = Column(Integer)



def init():
    engine = create_engine('sqlite:///base.sqlite', echo=True)

    Base.metadata.create_all(engine)

    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def add(shop, session):  #запись в базу данных
    session.add(shop)
    session.commit()

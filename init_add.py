from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tel = Column(Integer)
    address = Column(String)
    type = Column(String)

    chat_id = Column(Integer)
    message_id = Column(Integer)

    def _repr_(self):
        return "<Shop(name='%s', tel='%s', address='%s')>" % (self.name, self.tel, self.address)


def init():
    engine = create_engine('sqlite:///base.sqlite', echo=True)



    Base.metadata.create_all(engine)

    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def add(shop, session):
    session.add(shop)
    session.commit()

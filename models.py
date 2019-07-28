from datetime import datetime
from sqlalchemy import (create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, func, desc, and_)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


DB_URI = 'sqlite:///news.db'
Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    date = Column(DateTime)
    body = Column(String(50))
    deleted = Column(Boolean)

    def __init__(self, title, date, body, deleted):
        self.title = title
        self.date = date
        self.body = body
        self.deleted = deleted

    def __repr__(self):
        return f'<News(id={self.id}, title={self.title}, date={self.date}, body={self.body}, deleted={self.deleted})>'


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey('news.id'))
    title = Column(String(50))
    date = Column(DateTime)
    comment = Column(String(140))

    def __init__(self, news_id, title, date, comment):
        self.news_id = news_id
        self.title = title
        self.date = date
        self.comment = comment

    def __repr__(self):
        return f'<Comment(' \
               f'id={self.id}, news_id={self.news_id}, title={self.title}, date={self.date}, comment={self.comment})>'


def init_db():
    session.add(
        News(title='first', date=datetime.fromisoformat('2019-01-01T20:56:35'), body='The news', deleted=False))
    session.add(
        News(title='second', date=datetime.fromisoformat('2019-02-01T20:56:35'), body='The news', deleted=False))
    session.add(
        News(title='third', date=datetime.fromisoformat('2019-03-01T20:56:35'), body='The news', deleted=False))
    session.add(
        News(title='fourth', date=datetime.fromisoformat('2019-04-01T20:56:35'), body='The news', deleted=False))
    # Deleted news shouldn't be displayed
    session.add(
        News(title='fifth', date=datetime.fromisoformat('2019-04-01T20:56:35'), body='The news', deleted=True))
    session.add(
        News(title='sixth', date=datetime.fromisoformat('2019-04-01T20:56:35'), body='The news', deleted=True))
    # News that has not come yet
    session.add(
        News(title='seventh', date=datetime.fromisoformat('2019-08-01T20:56:35'), body='The news', deleted=False))

    session.add(
        Comments(title='first', date=datetime.fromisoformat('2019-01-01T20:56:35'), comment='The news', news_id=1))
    session.add(
        Comments(title='second', date=datetime.fromisoformat('2019-01-01T20:56:35'), comment='The news', news_id=2))
    session.add(
        Comments(title='third', date=datetime.fromisoformat('2019-03-01T20:56:35'), comment='The news', news_id=1))
    session.add(
        Comments(title='fourth', date=datetime.fromisoformat('2019-01-01T20:56:35'), comment='The news', news_id=3))
    session.add(
        Comments(title='fifth', date=datetime.fromisoformat('2019-01-01T20:56:35'), comment='The news', news_id=5))
    session.add(
        Comments(title='sixth', date=datetime.fromisoformat('2019-01-01T20:56:35'), comment='The news', news_id=6))

    session.commit()


# create and initialize database
if __name__ == '__main__':
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    init_db()

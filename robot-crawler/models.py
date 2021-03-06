#! /usr/local/bin/python
#coding:utf-8
from sqlalchemy import create_engine, func, ForeignKey, Column
from sqlalchemy.types import String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

__author__ = 'frostpeng'
 
engine = create_engine("mysql+mysqlconnector://robot:RoBOt%.%@localhost:3306/robot_web")
# support emoji(utf8mb4) 
# engine.execute("set names utf8mb4;")
MapBase = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)

#创建一个映射类
class Article(MapBase):
	__tablename__ = 'v2exArticle'
	art_id = Column(Integer, primary_key=True)
	art_url=Column(String(300), nullable=False)
	title=Column(Text,nullable=False)
	author=Column(String(200), nullable=False)
	author_url=Column(String(200), nullable=True)
	content=Column(Text, nullable=False)
	reply_count=Column(Integer,default=0)
	time_create=Column(String(20))
	time_modify=Column(String(20))
	source=Column(Integer,default=0)
	source_name=Column(Text,nullable=True)

MapBase.metadata.create_all(engine) 




ScopedSession = scoped_session(DBSession)

@contextmanager
def session_scope(scoped=True):
    """Provide a *thread-safe* transactional scope around a series of operations."""
    session = ScopedSession() if scoped else DBSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        # detach all instances in this session
        # and release connection
        session.close()


def getArticleByUrl(url):
	with session_scope() as session:
		article = session.query(Article).filter_by(art_url=url).first()
		return article
 

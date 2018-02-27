#!/usr/bin/env python

from io import StringIO
from os import linesep
from conf import conf
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, Integer, TEXT
import time


sa = conf.sqlalchemy

db_engine = create_engine(conf.mysql.unitymob, echo=sa.echo,
                          pool_size=sa.pool_size,
                          pool_recycle=sa.pool_recycle)

UnitymobSession = sessionmaker(bind=db_engine, autoflush=sa.autoflush)


class OriginalMapper(object):
    __table_args__ = {
        'mysql_charset': 'utf8mb4'
    }

    @property
    def dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def __str__(self) -> str:
        string = StringIO()
        string.writelines("============={classname}=============".format(classname=self.__class__.__name__) + linesep )
        for x in self.__dict__.keys():
            if x[0:1] == '_': continue
            string.writelines("{key} 的值为 {value}".format(key=x, value=self.__dict__[x]) + linesep )
        string.seek(0)
        desc = string.getvalue()
        string.close()
        return desc

class BaseMapper(OriginalMapper):
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(Integer)

BaseDO = declarative_base(cls=BaseMapper)


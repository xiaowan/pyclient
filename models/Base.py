#!/usr/bin/env python3.5

from library.Decorate import DI, Transaction
from library.G import G


@DI(g=G.getInstance())
class BaseModel(object):
    _instance = None

    def __init__(self):
        pass

    @property
    def session(self):
        return self.g.session

    @property
    def log(self):
        return self.g.log

    @property
    def utils(self):
        return self.g.utils

    @property
    def rabbitmq(self):
        return self.g.rabbitmq

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @Transaction(name="session")
    def save(self, obj):
        """ 保存对象，支持批量写入"""
        if isinstance(obj, list):
            res = self.session.add_all(obj)
        else:
            res = self.session.add(obj)
        self.session.flush()
        return res

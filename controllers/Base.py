#!/usr/bin/env python3.5

from library.Decorate import DI
from library.G import G


@DI(g=G.getInstance())
class BaseController(object):
    """ controller 基类 """
    _instance = None

    @property
    def rabbitmq(self):
        return self.g.rabbitmq

    @property
    def utils(self):
        return self.g.utils

    @property
    def log(self):
        return self.g.log

    @property
    def conf(self):
        return self.g.conf

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def prepare(self):
        """ 如果有需要预先执行的逻辑，写在prepare方法中 """
        pass

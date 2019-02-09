#!/usr/bin/env python

from .G import G
from .Decorate import DI
import logging

LOGGER = logging.getLogger(__file__)


class Classes(object):
    class SingletonMinix(object):
        """ 单例 """
        _instance = None

        @classmethod
        def getInstance(cls):
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    @DI(g=G.getInstance())
    class BaseMinix(SingletonMinix):
        """ 所有业务相关类的基类 """

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

        @property
        def mongo(self):
            return self.g.mongo

        @property
        def es(self):
            return self.g.es

        @property
        def redis(self):
            return self.g.redis

        def prepare(self):
            """ 如果有需要预先执行的逻辑，写在prepare方法中 """
            pass

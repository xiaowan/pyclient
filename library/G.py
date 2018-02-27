#!/usr/bin/env python


from conf import conf, log
from library.Utils import Utils
from library.MyRabbitmq import MyRabbitmq
from library.MyRedis import MyRedis

from mapper import UnitymobSession


class G(object):
    """ 全局类 """
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.conf = conf
        self.log = log
        self.utils = Utils
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = UnitymobSession()
        return self._session

    @property
    def rabbitmq(self):
        """ rabbitmq 操作句柄 """
        return MyRabbitmq.getInstance(conf.rabbitmq.dsn)

    @property
    def redis(self):
        return MyRedis.getInstance(conf.redis.host, conf.redis.port, conf.redis.password, False)

    def close(self):
        """ 善后清理工作 """
        # mysql
        if self._session is not None:
            self._session.close()

        # rabbitmq
        del self.rabbitmq.channel

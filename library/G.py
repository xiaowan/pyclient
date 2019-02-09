#!/usr/bin/env python

import threading

from conf import conf, log
from library.Utils import Utils
from library.MyRabbitmq import MyRabbitmq
from library.MyRedis import MyRedis
from library.MyMongo import MyMongo
from library.MyElasticsearch import MyElasticsearch

from mapper import UnitymobSession


class G(object):
    """ 全局类 """
    _instance = None
    _cleard = False

    def __init__(self):
        self.thread_local = threading.local()
        self.conf = conf
        self.utils = Utils
        self._caller = None

    @property
    def is_cleard(self):
        """ 请求结束，是否已经清理结尾 """
        return self._cleard

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
        if not hasattr(self.thread_local, '_session'):
            self.thread_local._session = UnitymobSession()
        return self.thread_local._session

    @property
    def rabbitmq(self):
        """ rabbitmq 操作句柄 """
        return MyRabbitmq.getInstance(conf.rabbitmq.dsn)

    @property
    def redis(self):
        return MyRedis.getInstance(conf.redis.host, conf.redis.port, conf.redis.password, False)

    @property
    def mongo(self):
        return MyMongo.getInstance(conf.mongo.dsn).get_mongodb_client

    @property
    def es(self):
        return MyElasticsearch.getInstance(conf.elasticsearch.dsn).get_es_client

    def close(self):
        """ 善后清理工作 """
        # mysql
        if hasattr(self.thread_local, '_session'):
            self.thread_local._session.close()

        # rabbitmq
        del self.rabbitmq.channel

        self._cleard = True
